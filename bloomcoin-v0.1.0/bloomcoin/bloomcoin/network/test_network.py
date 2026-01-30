"""
Test suite for BloomCoin network module.
"""

import asyncio
import unittest
import struct
import numpy as np
from unittest.mock import Mock, MagicMock, AsyncMock, patch

from .node import Node, Peer
from .gossip import (
    encode_phase_state,
    decode_phase_state,
    incorporate_peer_phases,
    merge_phase_states,
    GossipManager
)
from .sync import ChainSynchronizer, HeaderChain


class TestPhaseEncoding(unittest.TestCase):
    """Test phase state encoding/decoding."""

    def test_encode_decode_basic(self):
        """Test basic encode/decode of phase state."""
        phases = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        r = 0.75
        psi = 1.234

        encoded = encode_phase_state(phases, r, psi)
        decoded_phases, decoded_r, decoded_psi = decode_phase_state(encoded)

        self.assertAlmostEqual(decoded_r, r, places=5)
        self.assertAlmostEqual(decoded_psi, psi, places=5)
        np.testing.assert_array_almost_equal(decoded_phases, phases)

    def test_encode_decode_large(self):
        """Test encoding with downsampling for large arrays."""
        phases = np.random.uniform(0, 2*np.pi, 1000)
        r = 0.85
        psi = 2.345

        encoded = encode_phase_state(phases, r, psi)
        decoded_phases, decoded_r, decoded_psi = decode_phase_state(encoded)

        # Should be downsampled to 64
        self.assertEqual(len(decoded_phases), 64)
        self.assertAlmostEqual(decoded_r, r, places=5)
        self.assertAlmostEqual(decoded_psi, psi, places=5)

    def test_decode_invalid(self):
        """Test decoding invalid data."""
        with self.assertRaises(ValueError):
            decode_phase_state(b'invalid')

        with self.assertRaises(ValueError):
            decode_phase_state(b'short')


class TestPhaseIncorporation(unittest.TestCase):
    """Test phase incorporation algorithms."""

    def test_incorporate_peer_phases(self):
        """Test incorporating peer phases."""
        local = np.array([0, np.pi/2, np.pi, 3*np.pi/2])
        peer = np.array([np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4])

        result = incorporate_peer_phases(local, peer, weight=0.5)

        # Should be between local and peer
        self.assertEqual(len(result), len(local))
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result < 2*np.pi))

    def test_incorporate_different_sizes(self):
        """Test incorporating phases of different sizes."""
        local = np.random.uniform(0, 2*np.pi, 100)
        peer = np.random.uniform(0, 2*np.pi, 50)

        result = incorporate_peer_phases(local, peer, weight=0.1)

        self.assertEqual(len(result), len(local))

    def test_merge_multiple_states(self):
        """Test merging multiple phase states."""
        states = [
            (np.array([0, np.pi]), 0.5, 1.0),
            (np.array([np.pi/2, 3*np.pi/2]), 0.6, 0.5),
            (np.array([np.pi/4, 5*np.pi/4]), 0.7, 0.3)
        ]

        merged_phases, merged_r = merge_phase_states(states)

        self.assertEqual(len(merged_phases), 2)
        self.assertTrue(0 <= merged_r <= 1)


class TestNode(unittest.IsolatedAsyncioTestCase):
    """Test network node functionality."""

    async def test_node_creation(self):
        """Test creating a node."""
        node = Node(host='127.0.0.1', port=8333)
        self.assertEqual(node.host, '127.0.0.1')
        self.assertEqual(node.port, 8333)
        self.assertEqual(len(node.peers), 0)

    async def test_node_start_stop(self):
        """Test starting and stopping a node."""
        node = Node(host='127.0.0.1', port=8334)

        await node.start()
        self.assertIsNotNone(node.server)

        await node.stop()
        self.assertFalse(node.server.is_serving())

    async def test_peer_connection(self):
        """Test peer connection handling."""
        # Create two nodes
        node1 = Node(host='127.0.0.1', port=8335)
        node2 = Node(host='127.0.0.1', port=8336)

        try:
            # Start both nodes
            await node1.start()
            await node2.start()

            # Connect node2 to node1
            peer = await node2.connect('127.0.0.1', 8335)

            # Wait for handshake
            await asyncio.sleep(0.1)

            # Check connection
            self.assertIsNotNone(peer)
            self.assertEqual(node2.get_peer_count(), 1)

        finally:
            await node1.stop()
            await node2.stop()

    async def test_message_broadcast(self):
        """Test message broadcasting."""
        node = Node()

        # Create mock peers
        peer1 = AsyncMock(spec=Peer)
        peer2 = AsyncMock(spec=Peer)
        node.peers = {('1.1.1.1', 8333): peer1, ('2.2.2.2', 8333): peer2}

        # Broadcast message
        await node.broadcast(0x14, b'test_payload')

        # Both peers should receive
        peer1.send.assert_called_once_with(0x14, b'test_payload')
        peer2.send.assert_called_once_with(0x14, b'test_payload')

    async def test_message_broadcast_exclude(self):
        """Test message broadcasting with exclusion."""
        node = Node()

        # Create mock peers
        peer1 = AsyncMock(spec=Peer)
        peer2 = AsyncMock(spec=Peer)
        node.peers = {('1.1.1.1', 8333): peer1, ('2.2.2.2', 8333): peer2}

        # Broadcast excluding peer1
        await node.broadcast(0x14, b'test_payload', exclude=peer1)

        # Only peer2 should receive
        peer1.send.assert_not_called()
        peer2.send.assert_called_once_with(0x14, b'test_payload')


class TestGossipManager(unittest.IsolatedAsyncioTestCase):
    """Test gossip manager functionality."""

    async def test_gossip_eager_strategy(self):
        """Test eager gossip strategy."""
        node = Mock()
        node.broadcast = AsyncMock()

        gossip = GossipManager(node, strategy='eager')

        phases = np.random.uniform(0, 2*np.pi, 100)
        r = 0.6
        psi = 1.5

        shared = await gossip.maybe_share_phases(phases, r, psi)

        self.assertTrue(shared)
        node.broadcast.assert_called_once()

    async def test_gossip_threshold_strategy(self):
        """Test threshold gossip strategy."""
        node = Mock()
        node.broadcast = AsyncMock()

        gossip = GossipManager(node, strategy='threshold')

        phases = np.random.uniform(0, 2*np.pi, 100)

        # Small increase - shouldn't share
        shared = await gossip.maybe_share_phases(phases, 0.5, 1.0)
        self.assertFalse(shared)
        node.broadcast.assert_not_called()

        # Large increase - should share
        shared = await gossip.maybe_share_phases(phases, 0.6, 1.0)
        self.assertTrue(shared)
        node.broadcast.assert_called_once()

    async def test_gossip_bloom_strategy(self):
        """Test bloom gossip strategy."""
        node = Mock()
        node.broadcast = AsyncMock()

        gossip = GossipManager(node, strategy='bloom')

        phases = np.random.uniform(0, 2*np.pi, 100)

        # Far from threshold - shouldn't share
        shared = await gossip.maybe_share_phases(phases, 0.3, 1.0)
        self.assertFalse(shared)

        # Close to threshold - should share
        from ..constants import Z_C
        shared = await gossip.maybe_share_phases(phases, Z_C - 0.05, 1.0)
        self.assertTrue(shared)
        node.broadcast.assert_called_once()

    async def test_coherence_announcement(self):
        """Test coherence announcement."""
        node = Mock()
        node.broadcast = AsyncMock()

        gossip = GossipManager(node)

        await gossip.announce_coherence(0.75, 1.234)

        node.broadcast.assert_called_once()
        call_args = node.broadcast.call_args
        self.assertEqual(call_args[0][0], 0x22)  # MSG_COHERENCE

    def test_network_coherence_calculation(self):
        """Test network coherence calculation."""
        node = Mock()

        # Create mock peers with different coherences
        peer1 = Mock(coherence=0.5)
        peer2 = Mock(coherence=0.6)
        peer3 = Mock(coherence=0.7)
        node.peers = {
            ('1.1.1.1', 8333): peer1,
            ('2.2.2.2', 8333): peer2,
            ('3.3.3.3', 8333): peer3
        }

        gossip = GossipManager(node)
        avg_coherence = gossip.get_network_coherence()

        self.assertAlmostEqual(avg_coherence, 0.6, places=5)


class TestHeaderChain(unittest.TestCase):
    """Test header chain functionality."""

    def test_add_header_valid(self):
        """Test adding valid headers."""
        chain = HeaderChain()

        # Add first header
        header1 = {
            'hash': b'hash1',
            'prev_hash': b'genesis',
            'timestamp': 1000,
            'height': 1
        }
        self.assertTrue(chain.add_header(header1))

        # Add connected header
        header2 = {
            'hash': b'hash2',
            'prev_hash': b'hash1',
            'timestamp': 2000,
            'height': 2
        }
        self.assertTrue(chain.add_header(header2))

        self.assertEqual(len(chain.headers), 2)

    def test_add_header_invalid(self):
        """Test rejecting invalid headers."""
        chain = HeaderChain()

        # Add first header
        header1 = {
            'hash': b'hash1',
            'prev_hash': b'genesis',
            'timestamp': 1000,
            'height': 1
        }
        chain.add_header(header1)

        # Try to add disconnected header
        header2 = {
            'hash': b'hash2',
            'prev_hash': b'wrong',
            'timestamp': 2000,
            'height': 2
        }
        self.assertFalse(chain.add_header(header2))

        # Try to add header with decreasing timestamp
        header3 = {
            'hash': b'hash3',
            'prev_hash': b'hash1',
            'timestamp': 500,
            'height': 2
        }
        self.assertFalse(chain.add_header(header3))

    def test_validate_chain(self):
        """Test chain validation."""
        chain = HeaderChain()

        # Build valid chain
        headers = [
            {'hash': b'h1', 'prev_hash': b'genesis', 'timestamp': 1000},
            {'hash': b'h2', 'prev_hash': b'h1', 'timestamp': 2000},
            {'hash': b'h3', 'prev_hash': b'h2', 'timestamp': 3000}
        ]

        for h in headers:
            chain.headers.append(h)

        self.assertTrue(chain.validate_chain())

        # Break chain
        chain.headers[1]['prev_hash'] = b'wrong'
        self.assertFalse(chain.validate_chain())


class TestChainSynchronizer(unittest.IsolatedAsyncioTestCase):
    """Test chain synchronizer functionality."""

    async def test_find_best_peer(self):
        """Test finding best peer."""
        node = Mock()
        chain = Mock(height=10)

        syncer = ChainSynchronizer(node, chain)

        # Create mock peers with different heights
        peer1 = Mock(height=15)
        peer2 = Mock(height=20)
        peer3 = Mock(height=12)
        node.peers = {
            ('1.1.1.1', 8333): peer1,
            ('2.2.2.2', 8333): peer2,
            ('3.3.3.3', 8333): peer3
        }

        best = syncer._find_best_peer()
        self.assertEqual(best, peer2)

    async def test_sync_up_to_date(self):
        """Test sync when already up to date."""
        node = Mock()
        chain = Mock(height=10)

        syncer = ChainSynchronizer(node, chain)

        # All peers at same height
        peer = Mock(height=10)
        node.peers = {('1.1.1.1', 8333): peer}

        result = await syncer.sync()
        self.assertTrue(result)

    @patch('asyncio.sleep', new_callable=AsyncMock)
    async def test_sync_download(self, mock_sleep):
        """Test downloading blocks during sync."""
        node = Mock()
        chain = Mock(height=10)
        chain.get_block_by_height = Mock(return_value=None)

        syncer = ChainSynchronizer(node, chain)

        # Peer with higher chain
        peer = AsyncMock()
        peer.height = 15
        peer.address = ('1.1.1.1', 8333)
        node.peers = {('1.1.1.1', 8333): peer}

        # Mock header chain validation
        syncer.header_chain.validate_chain = Mock(return_value=True)
        syncer.header_chain.get_missing_blocks = Mock(return_value=[11, 12, 13, 14, 15])

        # Mock download methods
        syncer._download_headers = AsyncMock()
        syncer._download_blocks = AsyncMock()

        result = await syncer.sync()
        self.assertTrue(result)

        # Should have called download methods
        syncer._download_headers.assert_called_once()
        syncer._download_blocks.assert_called_once()


if __name__ == '__main__':
    unittest.main()