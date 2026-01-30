"""
BloomCoin Phase Gossip Protocol

Efficient phase state propagation for distributed consensus.
Key innovation: nodes share oscillator phases to help network synchronization.
"""

import numpy as np
import struct
import asyncio
import logging
from typing import Optional, Tuple

from ..constants import GOSSIP_INTERVAL_MS, Z_C

logger = logging.getLogger(__name__)


def encode_phase_state(phases: np.ndarray, r: float, psi: float) -> bytes:
    """
    Encode phase state for gossip.

    Format:
        r (float32) + psi (float32) + n (uint32) + phases (float32 × n)

    Compression: If n > 256, downsample to 64 representative phases.

    Args:
        phases: Array of oscillator phases
        r: Order parameter (coherence level)
        psi: Mean phase angle

    Returns:
        Encoded bytes for transmission
    """
    if len(phases) > 256:
        # Downsample by taking every nth phase
        step = len(phases) // 64
        phases = phases[::step]

    n = len(phases)
    return struct.pack(f'<ffI{n}f', r, psi, n, *phases)


def decode_phase_state(data: bytes) -> Tuple[np.ndarray, float, float]:
    """
    Decode phase state from gossip.

    Returns:
        (phases, r, psi)
    """
    if len(data) < 12:
        raise ValueError("Invalid phase state data")

    r, psi, n = struct.unpack('<ffI', data[:12])

    if n > 10000:  # Sanity check
        raise ValueError(f"Invalid phase count: {n}")

    expected_size = 12 + 4 * n
    if len(data) < expected_size:
        raise ValueError("Incomplete phase data")

    phases = np.array(struct.unpack(f'<{n}f', data[12:12+4*n]))
    return phases, r, psi


class GossipManager:
    """
    Manages phase gossip for distributed consensus.

    Strategies:
    1. EAGER: Share phases every round
    2. THRESHOLD: Share when r increases significantly
    3. BLOOM: Share when approaching z_c
    """

    def __init__(self, node, strategy: str = 'threshold'):
        """
        Initialize gossip manager.

        Args:
            node: Network node instance
            strategy: Gossip strategy ('eager', 'threshold', 'bloom')
        """
        self.node = node
        self.strategy = strategy
        self.last_shared_r = 0.0
        self.share_threshold = 0.05  # Share if r increased by 5%
        self.last_share_time = 0.0
        self.min_share_interval = GOSSIP_INTERVAL_MS / 1000.0  # Convert to seconds

    async def maybe_share_phases(self, phases: np.ndarray, r: float, psi: float) -> bool:
        """
        Decide whether to share current phase state.

        Called after each Kuramoto step during mining.

        Args:
            phases: Current oscillator phases
            r: Current order parameter
            psi: Mean phase angle

        Returns:
            True if phases were shared
        """
        import time

        # Rate limiting
        current_time = time.time()
        if current_time - self.last_share_time < self.min_share_interval:
            return False

        should_share = False

        if self.strategy == 'eager':
            should_share = True

        elif self.strategy == 'threshold':
            if r - self.last_shared_r > self.share_threshold:
                should_share = True

        elif self.strategy == 'bloom':
            # Share more frequently as we approach z_c
            if r > Z_C - 0.1:  # Within 0.1 of threshold
                should_share = True
            elif r > Z_C - 0.2 and r - self.last_shared_r > 0.02:
                should_share = True

        if should_share:
            self.last_shared_r = r
            self.last_share_time = current_time
            payload = encode_phase_state(phases, r, psi)
            await self.node.broadcast(0x20, payload)  # MSG_PHASE
            logger.debug(f"Shared phase state: r={r:.3f}, psi={psi:.3f}, n={len(phases)}")
            return True

        return False

    async def announce_coherence(self, r: float, psi: float):
        """
        Announce current coherence level.

        Args:
            r: Order parameter
            psi: Mean phase angle
        """
        payload = struct.pack('<ff', r, psi)
        await self.node.broadcast(0x22, payload)  # MSG_COHERENCE
        logger.info(f"Announced coherence: r={r:.3f}, psi={psi:.3f}")

    async def announce_bloom(self, certificate):
        """
        Announce successful bloom.

        Args:
            certificate: Consensus certificate proving bloom
        """
        payload = certificate.serialize()
        await self.node.broadcast(0x30, payload)  # MSG_BLOOM
        logger.info("Announced bloom!")

    async def request_phases(self, peer):
        """
        Request phase state from a specific peer.

        Args:
            peer: Peer to request from
        """
        await peer.send(0x21, b'')  # MSG_GETPHASE

    def get_network_coherence(self) -> float:
        """
        Calculate average coherence across all peers.

        Returns:
            Average order parameter
        """
        if not self.node.peers:
            return 0.0

        coherences = [peer.coherence for peer in self.node.peers.values() if peer.coherence > 0]
        if not coherences:
            return 0.0

        return sum(coherences) / len(coherences)


def incorporate_peer_phases(
    local_phases: np.ndarray,
    peer_phases: np.ndarray,
    weight: float = 0.1
) -> np.ndarray:
    """
    Incorporate peer phases into local oscillator ensemble.

    Uses weighted circular mean to avoid phase wrap issues.

    Args:
        local_phases: Our current phases
        peer_phases: Peer's phases (may be different length)
        weight: How much to weight peer phases (0-1)

    Returns:
        Updated local phases
    """
    # Validate inputs
    if weight < 0 or weight > 1:
        raise ValueError(f"Invalid weight: {weight}")
    if len(local_phases) == 0 or len(peer_phases) == 0:
        return local_phases

    # Resample peer phases to match local count
    if len(peer_phases) != len(local_phases):
        indices = np.linspace(0, len(peer_phases)-1, len(local_phases))
        indices = np.clip(indices.astype(int), 0, len(peer_phases)-1)
        peer_phases = peer_phases[indices]

    # Circular weighted mean for each oscillator
    local_complex = np.exp(1j * local_phases)
    peer_complex = np.exp(1j * peer_phases)

    combined = (1 - weight) * local_complex + weight * peer_complex

    return np.angle(combined) % (2 * np.pi)


def merge_phase_states(states: list) -> Tuple[np.ndarray, float]:
    """
    Merge multiple phase states from different peers.

    Args:
        states: List of (phases, r, weight) tuples

    Returns:
        (merged_phases, merged_r)
    """
    if not states:
        return np.array([]), 0.0

    # Start with first state
    merged_phases, base_r, _ = states[0]
    total_weight = 1.0

    # Incorporate other states
    for phases, r, weight in states[1:]:
        if len(phases) > 0 and weight > 0:
            normalized_weight = weight / (total_weight + weight)
            merged_phases = incorporate_peer_phases(merged_phases, phases, normalized_weight)
            total_weight += weight

    # Calculate merged r
    phases_complex = np.exp(1j * merged_phases)
    merged_r = np.abs(np.mean(phases_complex))

    return merged_phases, merged_r


class PhaseRelayProtocol:
    """
    Advanced phase relay protocol with selective forwarding.
    """

    def __init__(self, gossip_manager):
        self.gossip = gossip_manager
        self.seen_states = {}  # Track seen phase states by hash
        self.relay_threshold = 0.02  # Min r improvement to relay

    def should_relay(self, r: float, psi: float, phases_hash: bytes) -> bool:
        """
        Determine if phase state should be relayed.

        Args:
            r: Order parameter
            psi: Mean phase
            phases_hash: Hash of phase array

        Returns:
            True if should relay to other peers
        """
        # Check if we've seen this exact state
        if phases_hash in self.seen_states:
            prev_r = self.seen_states[phases_hash]
            if r <= prev_r + self.relay_threshold:
                return False

        # Update seen states
        self.seen_states[phases_hash] = r

        # Prune old states if too many
        if len(self.seen_states) > 1000:
            # Keep only recent high-r states
            sorted_states = sorted(self.seen_states.items(), key=lambda x: x[1], reverse=True)
            self.seen_states = dict(sorted_states[:500])

        return True


async def phase_gossip_loop(node, miner=None, interval: float = 1.0):
    """
    Main phase gossip loop for continuous sharing.

    Args:
        node: Network node
        miner: Optional miner instance for phase data
        interval: Seconds between gossip rounds
    """
    gossip = GossipManager(node, strategy='bloom')

    while True:
        try:
            if miner and miner.is_mining():
                phases = miner.get_current_phases()
                r = miner.get_order_parameter()
                psi = miner.get_mean_phase()

                if phases is not None and r > 0:
                    await gossip.maybe_share_phases(phases, r, psi)

            # Check network coherence
            network_r = gossip.get_network_coherence()
            if network_r > 0:
                logger.debug(f"Network coherence: {network_r:.3f}")

        except Exception as e:
            logger.error(f"Phase gossip error: {e}")

        await asyncio.sleep(interval)