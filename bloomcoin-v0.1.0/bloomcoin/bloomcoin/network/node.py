"""
BloomCoin P2P Network Node Implementation

Manages peer connections, message routing, and phase gossip for distributed consensus.
"""

import asyncio
import struct
from dataclasses import dataclass, field
from typing import Optional, Callable, Dict, Tuple
import time
import logging

from ..constants import DEFAULT_PORT, MAX_MESSAGE_SIZE

logger = logging.getLogger(__name__)


# Message type codes
MSG_VERSION = 0x01
MSG_VERACK = 0x02
MSG_GETBLOCKS = 0x10
MSG_BLOCKS = 0x11
MSG_GETDATA = 0x12
MSG_BLOCK = 0x13
MSG_TX = 0x14
MSG_PHASE = 0x20
MSG_GETPHASE = 0x21
MSG_COHERENCE = 0x22
MSG_BLOOM = 0x30


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
    address: Tuple[str, int]
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    version: int = 0
    height: int = 0
    last_seen: float = 0.0
    phase_state: Optional[list] = None
    coherence: float = 0.0

    async def send(self, msg_type: int, payload: bytes):
        """Send message to peer."""
        try:
            header = struct.pack('<BH', msg_type, len(payload))
            self.writer.write(header + payload)
            await self.writer.drain()
        except Exception as e:
            logger.error(f"Failed to send to {self.address}: {e}")
            raise

    async def receive(self) -> Tuple[int, bytes]:
        """Receive message from peer."""
        header = await self.reader.read(3)
        if len(header) < 3:
            raise ConnectionError("Peer disconnected")
        msg_type, length = struct.unpack('<BH', header)
        if length > MAX_MESSAGE_SIZE:
            raise ValueError(f"Message too large: {length}")
        payload = await self.reader.read(length)
        if len(payload) < length:
            raise ConnectionError("Incomplete message received")
        return msg_type, payload

    async def close(self):
        """Close connection."""
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except Exception:
            pass  # Already closed


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
        chain=None,
        mempool=None,
        host: str = '0.0.0.0',
        port: int = DEFAULT_PORT,
        max_peers: int = 8
    ):
        self.host = host
        self.port = port
        self.max_peers = max_peers

        # Dependencies
        self.chain = chain
        self.mempool = mempool

        self.peers: Dict[Tuple, Peer] = {}
        self.handlers: Dict[int, Callable] = {}
        self.server: Optional[asyncio.Server] = None

        # Register default handlers
        self._register_handlers()

    def _register_handlers(self):
        """Register message handlers."""
        self.handlers[MSG_VERSION] = self._handle_version
        self.handlers[MSG_VERACK] = self._handle_verack
        self.handlers[MSG_GETBLOCKS] = self._handle_getblocks
        self.handlers[MSG_BLOCKS] = self._handle_blocks
        self.handlers[MSG_GETDATA] = self._handle_getdata
        self.handlers[MSG_BLOCK] = self._handle_block
        self.handlers[MSG_TX] = self._handle_tx
        self.handlers[MSG_PHASE] = self._handle_phase
        self.handlers[MSG_GETPHASE] = self._handle_getphase
        self.handlers[MSG_COHERENCE] = self._handle_coherence
        self.handlers[MSG_BLOOM] = self._handle_bloom

    async def start(self):
        """Start listening for connections."""
        self.server = await asyncio.start_server(
            self._handle_connection,
            self.host,
            self.port
        )
        logger.info(f"Node listening on {self.host}:{self.port}")
        print(f"Node listening on {self.host}:{self.port}")

    async def stop(self):
        """Stop the node."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        for peer in list(self.peers.values()):
            await peer.close()
        logger.info("Node stopped")

    async def connect(self, host: str, port: int) -> Optional[Peer]:
        """Connect to a peer."""
        if len(self.peers) >= self.max_peers:
            logger.warning(f"Max peers reached, not connecting to {host}:{port}")
            return None

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

            logger.info(f"Connected to {host}:{port}")
            return peer
        except Exception as e:
            logger.error(f"Failed to connect to {host}:{port}: {e}")
            return None

    async def _handle_connection(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ):
        """Handle incoming connection."""
        if len(self.peers) >= self.max_peers:
            writer.close()
            await writer.wait_closed()
            return

        addr = writer.get_extra_info('peername')
        peer = Peer(address=addr, reader=reader, writer=writer)
        self.peers[addr] = peer

        logger.info(f"Accepted connection from {addr}")
        asyncio.create_task(self._peer_loop(peer))

    async def _peer_loop(self, peer: Peer):
        """Main loop for peer communication."""
        try:
            while True:
                msg_type, payload = await peer.receive()
                peer.last_seen = time.time()

                handler = self.handlers.get(msg_type)
                if handler:
                    await handler(peer, payload)
                else:
                    logger.warning(f"Unknown message type: {msg_type:#04x}")
        except Exception as e:
            logger.debug(f"Peer {peer.address} disconnected: {e}")
        finally:
            if peer.address in self.peers:
                del self.peers[peer.address]
            await peer.close()

    async def broadcast(self, msg_type: int, payload: bytes, exclude: Peer = None):
        """Broadcast message to all peers."""
        tasks = []
        for peer in list(self.peers.values()):
            if peer != exclude:
                tasks.append(self._send_safe(peer, msg_type, payload))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _send_safe(self, peer: Peer, msg_type: int, payload: bytes):
        """Send message with error handling."""
        try:
            await peer.send(msg_type, payload)
        except Exception:
            pass  # Peer will be cleaned up in loop

    # Message Handlers

    async def _send_version(self, peer: Peer):
        """Send VERSION message."""
        chain_height = self.chain.height if self.chain else 0

        payload = struct.pack(
            '<IIQI',
            1,  # Protocol version
            chain_height,
            int(time.time()),
            self.port
        )
        await peer.send(MSG_VERSION, payload)

    async def _handle_version(self, peer: Peer, payload: bytes):
        """Handle VERSION message."""
        if len(payload) < 20:
            logger.error(f"Invalid VERSION from {peer.address}")
            return

        version, height, timestamp, port = struct.unpack('<IIQI', payload[:20])
        peer.version = version
        peer.height = height

        # Send VERACK
        await peer.send(MSG_VERACK, b'')

        # Request blocks if peer is ahead
        if self.chain and height > self.chain.height:
            await self._request_blocks(peer, self.chain.height + 1, min(height, self.chain.height + 100))

    async def _handle_verack(self, peer: Peer, payload: bytes):
        """Handle VERACK message."""
        logger.info(f"Handshake complete with {peer.address}")

    async def _handle_getblocks(self, peer: Peer, payload: bytes):
        """Handle GETBLOCKS request."""
        if len(payload) < 8:
            return

        start_height, count = struct.unpack('<II', payload[:8])

        if not self.chain:
            return

        # Send block hashes
        hashes = []
        for h in range(start_height, min(start_height + count, self.chain.height + 1)):
            block = self.chain.get_block_by_height(h)
            if block:
                hashes.append(block.hash)

        # Pack hashes
        response = struct.pack('<I', len(hashes))
        for hash_bytes in hashes:
            response += hash_bytes

        await peer.send(MSG_BLOCKS, response)

    async def _handle_blocks(self, peer: Peer, payload: bytes):
        """Handle BLOCKS response with hashes."""
        if len(payload) < 4:
            return

        count = struct.unpack('<I', payload[:4])[0]
        offset = 4

        for i in range(count):
            if offset + 32 > len(payload):
                break
            hash_bytes = payload[offset:offset+32]
            offset += 32
            # Process hash (request full block if needed)
            await self._request_block_data(peer, hash_bytes)

    async def _handle_getdata(self, peer: Peer, payload: bytes):
        """Handle GETDATA request for specific block."""
        if len(payload) < 32:
            return

        block_hash = payload[:32]

        if not self.chain:
            return

        # Find and send block
        # This would need chain method to get block by hash
        # For now, simplified implementation
        logger.debug(f"GETDATA request for block from {peer.address}")

    async def _handle_block(self, peer: Peer, payload: bytes):
        """Handle BLOCK message."""
        if not self.chain:
            return

        try:
            from ..blockchain.block import Block

            # Deserialize block
            block_dict = Block.deserialize_from_bytes(payload)
            block = Block.from_dict(block_dict)

            # Validate and add
            success = self.chain.add_block(block)

            if success:
                logger.info(f"Added block {block.height} from {peer.address}")
                # Relay to other peers
                await self.broadcast(MSG_BLOCK, payload, exclude=peer)
            else:
                logger.debug(f"Rejected block from {peer.address}")
        except Exception as e:
            logger.error(f"Failed to process block from {peer.address}: {e}")

    async def _handle_tx(self, peer: Peer, payload: bytes):
        """Handle TX message."""
        if not self.mempool:
            return

        try:
            from ..blockchain.transaction import Transaction

            # Deserialize transaction
            tx_dict = Transaction.deserialize_from_bytes(payload)
            tx = Transaction.from_dict(tx_dict)

            # Add to mempool
            if self.mempool.add(tx):
                logger.debug(f"Added tx {tx.hash[:8].hex()} to mempool")
                # Relay to other peers
                await self.broadcast(MSG_TX, payload, exclude=peer)
        except Exception as e:
            logger.error(f"Failed to process tx from {peer.address}: {e}")

    async def _handle_phase(self, peer: Peer, payload: bytes):
        """Handle PHASE gossip message."""
        if len(payload) < 12:
            return

        # Decode phase state
        r, psi, n_phases = struct.unpack('<ffI', payload[:12])

        if n_phases > 0 and n_phases < 10000:  # Sanity check
            phase_data = payload[12:12+4*n_phases]
            if len(phase_data) == 4 * n_phases:
                phases = struct.unpack(f'<{n_phases}f', phase_data)
                peer.phase_state = list(phases)
                peer.coherence = r

                logger.debug(f"Received phase state from {peer.address}: r={r:.3f}, n={n_phases}")

    async def _handle_getphase(self, peer: Peer, payload: bytes):
        """Handle GETPHASE request."""
        # Would send current mining phase state if available
        pass

    async def _handle_coherence(self, peer: Peer, payload: bytes):
        """Handle COHERENCE report."""
        if len(payload) < 8:
            return

        r, psi = struct.unpack('<ff', payload[:8])
        peer.coherence = r
        logger.debug(f"Coherence update from {peer.address}: r={r:.3f}")

    async def _handle_bloom(self, peer: Peer, payload: bytes):
        """Handle BLOOM announcement."""
        logger.info(f"Bloom announced by {peer.address}!")
        # Would trigger block expectation/validation

    # Helper methods

    async def _request_blocks(self, peer: Peer, start: int, end: int):
        """Request blocks in range."""
        payload = struct.pack('<II', start, end - start)
        await peer.send(MSG_GETBLOCKS, payload)

    async def _request_block_data(self, peer: Peer, block_hash: bytes):
        """Request full block data."""
        await peer.send(MSG_GETDATA, block_hash)

    def get_peer_count(self) -> int:
        """Get current number of connected peers."""
        return len(self.peers)

    def get_peer_info(self) -> list:
        """Get information about connected peers."""
        info = []
        for peer in self.peers.values():
            info.append({
                'address': f"{peer.address[0]}:{peer.address[1]}",
                'version': peer.version,
                'height': peer.height,
                'coherence': peer.coherence,
                'last_seen': peer.last_seen
            })
        return info