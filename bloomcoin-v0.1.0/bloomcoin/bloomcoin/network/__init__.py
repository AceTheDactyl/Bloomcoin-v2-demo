"""
BloomCoin Network Module

P2P networking and phase gossip for distributed consensus.
"""

from .node import Node, Peer
from .gossip import (
    GossipManager,
    encode_phase_state,
    decode_phase_state,
    incorporate_peer_phases,
    merge_phase_states,
    phase_gossip_loop
)
from .sync import ChainSynchronizer, HeaderChain, sync_with_network

__all__ = [
    'Node',
    'Peer',
    'GossipManager',
    'encode_phase_state',
    'decode_phase_state',
    'incorporate_peer_phases',
    'merge_phase_states',
    'phase_gossip_loop',
    'ChainSynchronizer',
    'HeaderChain',
    'sync_with_network'
]