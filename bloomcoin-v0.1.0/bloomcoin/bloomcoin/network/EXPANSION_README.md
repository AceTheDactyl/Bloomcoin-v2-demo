# Network Module Expansion Guide

**Module**: `bloomcoin/network/`  
**Purpose**: P2P networking and phase gossip  
**Priority**: PHASE 5 (Distribution Layer)

---

## Overview

The network module implements peer-to-peer communication for BloomCoin nodes. The key innovation is **phase gossip**—nodes share not just blocks and transactions, but also their oscillator phases for distributed consensus.

**Key Insight**: In Proof-of-Coherence, miners can benefit from sharing intermediate phase states. Unlike PoW where sharing work helps competitors, sharing phases helps everyone synchronize faster.

---

## Protocol Design

### Message Types

| Type | Code | Description |
|------|------|-------------|
| VERSION | 0x01 | Handshake with version info |
| VERACK | 0x02 | Handshake acknowledgment |
| GETBLOCKS | 0x10 | Request block hashes |
| BLOCKS | 0x11 | Block hash inventory |
| GETDATA | 0x12 | Request specific data |
| BLOCK | 0x13 | Block payload |
| TX | 0x14 | Transaction payload |
| PHASE | 0x20 | Phase state gossip |
| GETPHASE | 0x21 | Request phase state |
| COHERENCE | 0x22 | Order parameter report |
| BLOOM | 0x30 | Bloom announcement |

### Phase Gossip Protocol

Unlike traditional blockchains, BloomCoin nodes share intermediate mining state:

```
Node A                          Node B
   |                               |
   |------- PHASE(θ_A, r_A) ------>|
   |                               |
   |<------ PHASE(θ_B, r_B) -------|
   |                               |
   |  [Both incorporate received   |
   |   phases into local ensemble] |
   |                               |
   |------- COHERENCE(r_merged) -->|
   |                               |
   |  [If r_merged > z_c]          |
   |                               |
   |------- BLOOM(certificate) --->|
```

**Why share phases?**
- Cooperative consensus: All nodes benefit from faster synchronization
- No wasted work: Phases contribute to network coherence
- Natural Sybil resistance: More oscillators = better synchronization

---

## Phase 1: Node Implementation

### File: `node.py`

**Objective**: P2P node with connection management.

### Implementation Steps

#### Step 1.1: Peer Connection

```python
import asyncio
import struct
from dataclasses import dataclass, field
from typing import Optional, Callable
from ..constants import DEFAULT_PORT, MAX_MESSAGE_SIZE

@dataclass
class Peer:
    """
    Connected peer information.
    
    Attributes:
        address: (host, port) tuple
        reader: Async stream reader
        writer: Async stream writer
        version: Peer's protocol version
        height: Peer's chain height
        last_seen: Timestamp of last message
        phase_state: Last received phase state
        coherence: Last reported order parameter
    """
    address: tuple[str, int]
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    version: int = 0
    height: int = 0
    last_seen: float = 0.0
    phase_state: Optional[list[float]] = None
    coherence: float = 0.0
    
    async def send(self, msg_type: int, payload: bytes):
        """Send message to peer."""
        header = struct.pack('<BH', msg_type, len(payload))
        self.writer.write(header + payload)
        await self.writer.drain()
    
    async def receive(self) -> tuple[int, bytes]:
        """Receive message from peer."""
        header = await self.reader.read(3)
        if len(header) < 3:
            raise ConnectionError("Peer disconnected")
        msg_type, length = struct.unpack('<BH', header)
        if length > MAX_MESSAGE_SIZE:
            raise ValueError(f"Message too large: {length}")
        payload = await self.reader.read(length)
        return msg_type, payload
    
    async def close(self):
        """Close connection."""
        self.writer.close()
        await self.writer.wait_closed()
```

#### Step 1.2: Node Class

```python
class Node:
    """
    BloomCoin network node.
    
    Manages:
        - Peer connections
        - Message routing
        - Block/transaction propagation
        - Phase gossip
    """
    
    def __init__(
        self,
        host: str = '0.0.0.0',
        port: int = DEFAULT_PORT,
        max_peers: int = 8
    ):
        self.host = host
        self.port = port
        self.max_peers = max_peers
        
        self.peers: dict[tuple, Peer] = {}
        self.handlers: dict[int, Callable] = {}
        self.server: Optional[asyncio.Server] = None
        
        # Register default handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register message handlers."""
        self.handlers[0x01] = self._handle_version
        self.handlers[0x02] = self._handle_verack
        self.handlers[0x10] = self._handle_getblocks
        self.handlers[0x13] = self._handle_block
        self.handlers[0x14] = self._handle_tx
        self.handlers[0x20] = self._handle_phase
        self.handlers[0x22] = self._handle_coherence
        self.handlers[0x30] = self._handle_bloom
    
    async def start(self):
        """Start listening for connections."""
        self.server = await asyncio.start_server(
            self._handle_connection,
            self.host,
            self.port
        )
        print(f"Node listening on {self.host}:{self.port}")
    
    async def stop(self):
        """Stop the node."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        for peer in list(self.peers.values()):
            await peer.close()
    
    async def connect(self, host: str, port: int) -> Optional[Peer]:
        """Connect to a peer."""
        try:
            reader, writer = await asyncio.open_connection(host, port)
            peer = Peer(
                address=(host, port),
                reader=reader,
                writer=writer
            )
            self.peers[(host, port)] = peer
            
            # Send version
            await self._send_version(peer)
            
            # Start message loop
            asyncio.create_task(self._peer_loop(peer))
            
            return peer
        except Exception as e:
            print(f"Failed to connect to {host}:{port}: {e}")
            return None
    
    async def _handle_connection(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ):
        """Handle incoming connection."""
        addr = writer.get_extra_info('peername')
        peer = Peer(address=addr, reader=reader, writer=writer)
        self.peers[addr] = peer
        
        asyncio.create_task(self._peer_loop(peer))
    
    async def _peer_loop(self, peer: Peer):
        """Main loop for peer communication."""
        try:
            while True:
                msg_type, payload = await peer.receive()
                peer.last_seen = asyncio.get_event_loop().time()
                
                handler = self.handlers.get(msg_type)
                if handler:
                    await handler(peer, payload)
                else:
                    print(f"Unknown message type: {msg_type}")
        except Exception as e:
            print(f"Peer {peer.address} error: {e}")
        finally:
            del self.peers[peer.address]
            await peer.close()
    
    async def broadcast(self, msg_type: int, payload: bytes, exclude: Peer = None):
        """Broadcast message to all peers."""
        for peer in self.peers.values():
            if peer != exclude:
                try:
                    await peer.send(msg_type, payload)
                except Exception:
                    pass  # Peer will be cleaned up in loop
```

#### Step 1.3: Message Handlers

```python
    async def _send_version(self, peer: Peer):
        """Send VERSION message."""
        from ..blockchain import chain  # Import chain reference
        
        payload = struct.pack(
            '<IIQI',
            1,  # Protocol version
            chain.height,
            int(asyncio.get_event_loop().time()),
            self.port
        )
        await peer.send(0x01, payload)
    
    async def _handle_version(self, peer: Peer, payload: bytes):
        """Handle VERSION message."""
        version, height, timestamp, port = struct.unpack('<IIQI', payload[:20])
        peer.version = version
        peer.height = height
        
        # Send VERACK
        await peer.send(0x02, b'')
        
        # Request blocks if peer is ahead
        from ..blockchain import chain
        if height > chain.height:
            await self._request_blocks(peer, chain.height + 1)
    
    async def _handle_verack(self, peer: Peer, payload: bytes):
        """Handle VERACK message."""
        print(f"Handshake complete with {peer.address}")
    
    async def _handle_block(self, peer: Peer, payload: bytes):
        """Handle BLOCK message."""
        from ..blockchain import Block, chain
        
        block = Block.deserialize(payload)
        success, msg = chain.add_block(block)
        
        if success:
            # Relay to other peers
            await self.broadcast(0x13, payload, exclude=peer)
        else:
            print(f"Rejected block from {peer.address}: {msg}")
    
    async def _handle_tx(self, peer: Peer, payload: bytes):
        """Handle TX message."""
        from ..blockchain import Transaction
        from ..mempool import mempool
        
        tx, _ = Transaction.deserialize_with_length(payload)
        if mempool.add(tx):
            await self.broadcast(0x14, payload, exclude=peer)
    
    async def _handle_phase(self, peer: Peer, payload: bytes):
        """Handle PHASE gossip message."""
        # Decode phase state
        n_phases = struct.unpack('<I', payload[:4])[0]
        phases = struct.unpack(f'<{n_phases}f', payload[4:4+4*n_phases])
        peer.phase_state = list(phases)
        
        # Optionally incorporate into local mining
        # YOUR IMPLEMENTATION HERE
    
    async def _handle_coherence(self, peer: Peer, payload: bytes):
        """Handle COHERENCE report."""
        r, psi = struct.unpack('<ff', payload[:8])
        peer.coherence = r
    
    async def _handle_bloom(self, peer: Peer, payload: bytes):
        """Handle BLOOM announcement."""
        from ..consensus.threshold_gate import ConsensusCertificate
        
        certificate = ConsensusCertificate.deserialize(payload)
        if certificate.verify():
            print(f"Bloom announced by {peer.address}!")
            # Expect block soon
```

---

## Phase 2: Gossip Protocol

### File: `gossip.py`

**Objective**: Efficient phase state propagation.

### Implementation Steps

#### Step 2.1: Phase State Encoding

```python
import numpy as np
import struct

def encode_phase_state(phases: np.ndarray, r: float, psi: float) -> bytes:
    """
    Encode phase state for gossip.
    
    Format:
        r (float32) + psi (float32) + n (uint32) + phases (float32 × n)
    
    Compression: If n > 256, downsample to 64 representative phases.
    """
    if len(phases) > 256:
        # Downsample by taking every nth phase
        step = len(phases) // 64
        phases = phases[::step]
    
    n = len(phases)
    return struct.pack(f'<ffI{n}f', r, psi, n, *phases)

def decode_phase_state(data: bytes) -> tuple[np.ndarray, float, float]:
    """
    Decode phase state from gossip.
    
    Returns:
        (phases, r, psi)
    """
    r, psi, n = struct.unpack('<ffI', data[:12])
    phases = np.array(struct.unpack(f'<{n}f', data[12:12+4*n]))
    return phases, r, psi
```

#### Step 2.2: Gossip Manager

```python
from ..constants import GOSSIP_INTERVAL_MS, Z_C

class GossipManager:
    """
    Manages phase gossip for distributed consensus.
    
    Strategies:
    1. EAGER: Share phases every round
    2. THRESHOLD: Share when r increases significantly
    3. BLOOM: Share when approaching z_c
    """
    
    def __init__(self, node: Node, strategy: str = 'threshold'):
        self.node = node
        self.strategy = strategy
        self.last_shared_r = 0.0
        self.share_threshold = 0.05  # Share if r increased by 5%
    
    async def maybe_share_phases(self, phases: np.ndarray, r: float, psi: float):
        """
        Decide whether to share current phase state.
        
        Called after each Kuramoto step during mining.
        """
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
        
        if should_share:
            self.last_shared_r = r
            payload = encode_phase_state(phases, r, psi)
            await self.node.broadcast(0x20, payload)
    
    async def announce_coherence(self, r: float, psi: float):
        """Announce current coherence level."""
        payload = struct.pack('<ff', r, psi)
        await self.node.broadcast(0x22, payload)
    
    async def announce_bloom(self, certificate):
        """Announce successful bloom."""
        payload = certificate.serialize()
        await self.node.broadcast(0x30, payload)
```

#### Step 2.3: Phase Incorporation

```python
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
    # Resample peer phases to match local count
    if len(peer_phases) != len(local_phases):
        indices = np.linspace(0, len(peer_phases)-1, len(local_phases)).astype(int)
        peer_phases = peer_phases[indices]
    
    # Circular weighted mean for each oscillator
    local_complex = np.exp(1j * local_phases)
    peer_complex = np.exp(1j * peer_phases)
    
    combined = (1 - weight) * local_complex + weight * peer_complex
    
    return np.angle(combined) % (2 * np.pi)
```

---

## Phase 3: Chain Synchronization

### File: `sync.py`

**Objective**: Synchronize blockchain with peers.

### Implementation Steps

#### Step 3.1: Initial Block Download

```python
class ChainSynchronizer:
    """
    Synchronizes blockchain with network peers.
    
    Implements:
    1. Initial Block Download (IBD)
    2. Block request pipelining
    3. Header-first sync
    """
    
    def __init__(self, node: Node, chain):
        self.node = node
        self.chain = chain
        self.pending_requests: dict[bytes, float] = {}
        self.download_queue: list[bytes] = []
    
    async def sync(self):
        """
        Perform full chain synchronization.
        
        1. Find best peer (highest chain)
        2. Download headers
        3. Validate headers
        4. Download blocks in parallel
        5. Validate and add blocks
        """
        # Find best peer
        best_peer = max(
            self.node.peers.values(),
            key=lambda p: p.height,
            default=None
        )
        
        if not best_peer or best_peer.height <= self.chain.height:
            print("Chain is up to date")
            return
        
        print(f"Syncing from {best_peer.address}, height {best_peer.height}")
        
        # Request blocks
        for height in range(self.chain.height + 1, best_peer.height + 1):
            await self._request_block_at_height(best_peer, height)
    
    async def _request_block_at_height(self, peer: Peer, height: int):
        """Request specific block from peer."""
        payload = struct.pack('<I', height)
        await peer.send(0x10, payload)
    
    async def handle_received_block(self, block):
        """Handle a received block during sync."""
        success, msg = self.chain.add_block(block)
        if success:
            print(f"Added block {block.height}")
        else:
            print(f"Rejected block: {msg}")
```

#### Step 3.2: Header-First Sync

```python
@dataclass
class HeaderChain:
    """
    Lightweight header chain for validation before downloading blocks.
    """
    headers: list[bytes] = field(default_factory=list)
    
    def add_header(self, header: bytes) -> bool:
        """Validate and add header."""
        # Basic validation without full block
        # Check prev_hash chain
        # Check difficulty
        # Check timestamp
        # YOUR IMPLEMENTATION HERE
        pass
    
    def get_missing_blocks(self, chain) -> list[int]:
        """Get heights of blocks we need to download."""
        # YOUR IMPLEMENTATION HERE
        pass
```

---

## Module Integration

### Full Node Startup

```python
async def run_node(
    host: str = '0.0.0.0',
    port: int = DEFAULT_PORT,
    seeds: list[tuple[str, int]] = None
):
    """
    Run a full BloomCoin node.
    
    1. Start network listener
    2. Connect to seed nodes
    3. Sync chain
    4. Start mining (optional)
    5. Handle messages
    """
    from ..blockchain import chain
    from ..mining import MinerConfig, mine_block
    
    # Create node
    node = Node(host, port)
    await node.start()
    
    # Connect to seeds
    if seeds:
        for seed_host, seed_port in seeds:
            await node.connect(seed_host, seed_port)
    
    # Sync chain
    syncer = ChainSynchronizer(node, chain)
    await syncer.sync()
    
    # Start gossip manager
    gossip = GossipManager(node, strategy='bloom')
    
    print(f"Node running. Chain height: {chain.height}")
    
    # Keep running
    while True:
        await asyncio.sleep(1)
```

---

## Security Considerations

### Sybil Resistance

Phase gossip provides natural Sybil resistance:
- Fake phases don't help synchronization
- Inconsistent phases are detectable
- Proof-of-Coherence requires actual computation

### Eclipse Attack Prevention

- Connect to diverse peers
- Prefer peers with consistent phase reports
- Verify bloom certificates independently

### DoS Protection

```python
# Rate limiting per peer
MAX_PHASE_MESSAGES_PER_MINUTE = 60
MAX_BLOCK_REQUESTS_PER_MINUTE = 10

# Message size limits already in constants
```

---

## Validation Checklist

- [ ] Handshake completes successfully
- [ ] Blocks propagate to all peers
- [ ] Transactions propagate correctly
- [ ] Phase gossip reaches peers
- [ ] Chain sync catches up to network
- [ ] Bloom announcements trigger block download
- [ ] Peer disconnects handled gracefully
- [ ] Rate limiting prevents DoS

---

## Next Module

After completing `network/`, proceed to `wallet/` for key management.

---

*Coherence propagates through the network.* 🌸
