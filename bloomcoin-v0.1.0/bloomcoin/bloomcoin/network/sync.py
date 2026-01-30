"""
BloomCoin Chain Synchronization

Synchronizes blockchain with network peers using header-first approach.
"""

import asyncio
import struct
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
import time

logger = logging.getLogger(__name__)


@dataclass
class HeaderChain:
    """
    Lightweight header chain for validation before downloading blocks.
    """
    headers: List[Dict] = field(default_factory=list)

    def add_header(self, header: Dict) -> bool:
        """
        Validate and add header.

        Args:
            header: Block header dict

        Returns:
            True if header was added successfully
        """
        # Basic validation without full block
        if not header:
            return False

        # Check prev_hash chain
        if self.headers:
            last_header = self.headers[-1]
            if header.get('prev_hash') != last_header.get('hash'):
                logger.error("Header doesn't connect to chain")
                return False

        # Check timestamp (must be increasing)
        if self.headers:
            if header.get('timestamp', 0) <= self.headers[-1].get('timestamp', 0):
                logger.error("Header timestamp not increasing")
                return False

        # Check difficulty meets requirements
        # This would need actual difficulty validation
        # Simplified for now

        self.headers.append(header)
        return True

    def get_missing_blocks(self, chain) -> List[int]:
        """
        Get heights of blocks we need to download.

        Args:
            chain: Current blockchain instance

        Returns:
            List of block heights to download
        """
        missing = []
        current_height = chain.height if chain else 0

        for i, header in enumerate(self.headers):
            header_height = header.get('height', i)
            if header_height > current_height:
                missing.append(header_height)

        return missing

    def validate_chain(self) -> bool:
        """
        Validate the header chain integrity.

        Returns:
            True if chain is valid
        """
        if not self.headers:
            return True

        for i in range(1, len(self.headers)):
            if self.headers[i].get('prev_hash') != self.headers[i-1].get('hash'):
                return False

        return True


class ChainSynchronizer:
    """
    Synchronizes blockchain with network peers.

    Implements:
    1. Initial Block Download (IBD)
    2. Block request pipelining
    3. Header-first sync
    """

    def __init__(self, node, chain):
        """
        Initialize synchronizer.

        Args:
            node: Network node instance
            chain: Blockchain instance
        """
        self.node = node
        self.chain = chain
        self.pending_requests: Dict[bytes, float] = {}
        self.download_queue: List[int] = []
        self.syncing = False
        self.header_chain = HeaderChain()
        self.max_blocks_per_request = 100
        self.request_timeout = 30.0  # seconds

    async def sync(self) -> bool:
        """
        Perform full chain synchronization.

        1. Find best peer (highest chain)
        2. Download headers
        3. Validate headers
        4. Download blocks in parallel
        5. Validate and add blocks

        Returns:
            True if sync completed successfully
        """
        if self.syncing:
            logger.warning("Already syncing")
            return False

        self.syncing = True

        try:
            # Find best peer
            best_peer = self._find_best_peer()

            if not best_peer:
                logger.info("No peers available for sync")
                return False

            if best_peer.height <= self.chain.height:
                logger.info("Chain is up to date")
                return True

            logger.info(f"Syncing from {best_peer.address}, height {best_peer.height}")

            # Download headers first
            await self._download_headers(best_peer)

            # Validate header chain
            if not self.header_chain.validate_chain():
                logger.error("Invalid header chain")
                return False

            # Get list of missing blocks
            missing_blocks = self.header_chain.get_missing_blocks(self.chain)

            if not missing_blocks:
                logger.info("No blocks to download")
                return True

            logger.info(f"Downloading {len(missing_blocks)} blocks")

            # Download blocks in batches
            await self._download_blocks(best_peer, missing_blocks)

            logger.info("Sync completed successfully")
            return True

        except Exception as e:
            logger.error(f"Sync failed: {e}")
            return False
        finally:
            self.syncing = False

    def _find_best_peer(self):
        """
        Find peer with highest chain.

        Returns:
            Best peer or None
        """
        if not self.node.peers:
            return None

        return max(
            self.node.peers.values(),
            key=lambda p: p.height,
            default=None
        )

    async def _download_headers(self, peer):
        """
        Download headers from peer.

        Args:
            peer: Peer to download from
        """
        start_height = self.chain.height + 1
        end_height = peer.height

        # Request headers in batches
        batch_size = 500
        for batch_start in range(start_height, end_height + 1, batch_size):
            batch_end = min(batch_start + batch_size - 1, end_height)
            await self._request_headers(peer, batch_start, batch_end)
            # Wait for headers to arrive (simplified)
            await asyncio.sleep(0.5)

    async def _request_headers(self, peer, start: int, end: int):
        """
        Request headers in range.

        Args:
            peer: Peer to request from
            start: Start height
            end: End height
        """
        payload = struct.pack('<II', start, end - start + 1)
        await peer.send(0x10, payload)  # MSG_GETBLOCKS

    async def _download_blocks(self, peer, heights: List[int]):
        """
        Download blocks at specified heights.

        Args:
            peer: Peer to download from
            heights: List of block heights to download
        """
        # Download in batches to avoid overwhelming peer
        batch_size = 10

        for i in range(0, len(heights), batch_size):
            batch = heights[i:i+batch_size]
            await self._download_block_batch(peer, batch)

    async def _download_block_batch(self, peer, heights: List[int]):
        """
        Download a batch of blocks.

        Args:
            peer: Peer to download from
            heights: Block heights to download
        """
        tasks = []
        for height in heights:
            tasks.append(self._request_and_wait_for_block(peer, height))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to download block {heights[i]}: {result}")

    async def _request_and_wait_for_block(self, peer, height: int) -> bool:
        """
        Request a block and wait for response.

        Args:
            peer: Peer to request from
            height: Block height

        Returns:
            True if block received and added
        """
        # Request block
        await self._request_block_at_height(peer, height)

        # Wait for block (simplified - real implementation would use futures)
        timeout = 5.0
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.chain.height >= height:
                return True
            await asyncio.sleep(0.1)

        logger.warning(f"Timeout waiting for block {height}")
        return False

    async def _request_block_at_height(self, peer, height: int):
        """
        Request specific block from peer.

        Args:
            peer: Peer to request from
            height: Block height
        """
        payload = struct.pack('<I', height)
        await peer.send(0x12, payload)  # MSG_GETDATA
        self.pending_requests[height.to_bytes(4, 'big')] = time.time()

    async def handle_received_block(self, block) -> bool:
        """
        Handle a received block during sync.

        Args:
            block: Block instance

        Returns:
            True if block was added successfully
        """
        try:
            # Remove from pending if present
            block_key = block.height.to_bytes(4, 'big')
            if block_key in self.pending_requests:
                del self.pending_requests[block_key]

            # Validate and add to chain
            success = self.chain.add_block(block)

            if success:
                logger.info(f"Added block {block.height}")
            else:
                logger.warning(f"Rejected block {block.height}")

            return success

        except Exception as e:
            logger.error(f"Failed to handle block: {e}")
            return False

    def cleanup_pending_requests(self):
        """Remove timed-out pending requests."""
        current_time = time.time()
        expired = []

        for key, request_time in self.pending_requests.items():
            if current_time - request_time > self.request_timeout:
                expired.append(key)

        for key in expired:
            del self.pending_requests[key]

        if expired:
            logger.debug(f"Cleaned up {len(expired)} expired requests")

    async def continuous_sync(self):
        """
        Continuously sync with network.

        Runs as background task.
        """
        while True:
            try:
                # Clean up old requests
                self.cleanup_pending_requests()

                # Check if we need to sync
                best_peer = self._find_best_peer()
                if best_peer and best_peer.height > self.chain.height:
                    await self.sync()

                # Wait before next sync check
                await asyncio.sleep(10)

            except Exception as e:
                logger.error(f"Continuous sync error: {e}")
                await asyncio.sleep(30)


class BlockValidator:
    """
    Validates blocks during synchronization.
    """

    @staticmethod
    def validate_header(header: Dict, prev_header: Optional[Dict] = None) -> bool:
        """
        Validate block header.

        Args:
            header: Header to validate
            prev_header: Previous header (if available)

        Returns:
            True if header is valid
        """
        # Check required fields
        required_fields = ['hash', 'prev_hash', 'timestamp', 'height']
        for field in required_fields:
            if field not in header:
                logger.error(f"Missing required field: {field}")
                return False

        # Check connection to previous
        if prev_header:
            if header['prev_hash'] != prev_header['hash']:
                logger.error("Header doesn't connect to previous")
                return False

            if header['height'] != prev_header['height'] + 1:
                logger.error("Invalid height progression")
                return False

            if header['timestamp'] <= prev_header['timestamp']:
                logger.error("Timestamp not increasing")
                return False

        return True

    @staticmethod
    def validate_block_batch(blocks: List) -> bool:
        """
        Validate a batch of blocks.

        Args:
            blocks: List of blocks to validate

        Returns:
            True if all blocks are valid and properly connected
        """
        if not blocks:
            return True

        for i in range(len(blocks)):
            if i > 0:
                # Check connection
                if blocks[i].prev_hash != blocks[i-1].hash:
                    logger.error(f"Block {i} doesn't connect to previous")
                    return False

            # Individual block validation would go here
            # (merkle root, transactions, etc.)

        return True


async def sync_with_network(node, chain, interval: float = 30.0):
    """
    Main synchronization loop.

    Args:
        node: Network node
        chain: Blockchain instance
        interval: Seconds between sync attempts
    """
    synchronizer = ChainSynchronizer(node, chain)

    # Initial sync
    await synchronizer.sync()

    # Continuous sync
    while True:
        try:
            await asyncio.sleep(interval)

            # Check if sync needed
            if node.get_peer_count() > 0:
                best_peer = synchronizer._find_best_peer()
                if best_peer and best_peer.height > chain.height + 1:
                    logger.info(f"Chain behind network, syncing...")
                    await synchronizer.sync()

        except Exception as e:
            logger.error(f"Sync loop error: {e}")
            await asyncio.sleep(interval)