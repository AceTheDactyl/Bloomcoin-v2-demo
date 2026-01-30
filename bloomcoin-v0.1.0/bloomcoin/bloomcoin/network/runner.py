"""
BloomCoin Network Runner

Run a full BloomCoin node with P2P networking and phase gossip.
"""

import asyncio
import argparse
import logging
import sys
from typing import List, Tuple, Optional

from .node import Node
from .gossip import GossipManager, phase_gossip_loop
from .sync import sync_with_network
from ..constants import DEFAULT_PORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def run_node(
    host: str = '0.0.0.0',
    port: int = DEFAULT_PORT,
    seeds: Optional[List[Tuple[str, int]]] = None,
    chain=None,
    mempool=None,
    miner=None
):
    """
    Run a full BloomCoin node.

    1. Start network listener
    2. Connect to seed nodes
    3. Sync chain
    4. Start mining (optional)
    5. Handle messages

    Args:
        host: Host to bind to
        port: Port to listen on
        seeds: List of (host, port) tuples for seed nodes
        chain: Blockchain instance
        mempool: Mempool instance
        miner: Miner instance (optional)
    """
    # Create node
    node = Node(
        chain=chain,
        mempool=mempool,
        host=host,
        port=port
    )

    try:
        # Start listening
        await node.start()
        logger.info(f"Node started on {host}:{port}")

        # Connect to seed nodes
        if seeds:
            logger.info(f"Connecting to {len(seeds)} seed nodes...")
            for seed_host, seed_port in seeds:
                try:
                    peer = await node.connect(seed_host, seed_port)
                    if peer:
                        logger.info(f"Connected to {seed_host}:{seed_port}")
                except Exception as e:
                    logger.error(f"Failed to connect to {seed_host}:{seed_port}: {e}")

        # Wait a moment for handshakes
        await asyncio.sleep(2)

        # Start chain sync if we have a chain
        sync_task = None
        if chain:
            logger.info("Starting chain synchronization...")
            sync_task = asyncio.create_task(sync_with_network(node, chain))

        # Start phase gossip if we have a miner
        gossip_task = None
        if miner:
            logger.info("Starting phase gossip...")
            gossip_task = asyncio.create_task(phase_gossip_loop(node, miner))

        logger.info(f"Node running. Chain height: {chain.height if chain else 0}")
        logger.info(f"Connected peers: {node.get_peer_count()}")

        # Keep running
        while True:
            await asyncio.sleep(10)

            # Log status
            peer_count = node.get_peer_count()
            chain_height = chain.height if chain else 0
            logger.debug(f"Status: {peer_count} peers, height {chain_height}")

            # Show peer info
            if peer_count > 0:
                peer_info = node.get_peer_info()
                for info in peer_info:
                    logger.debug(f"  Peer {info['address']}: height={info['height']}, r={info['coherence']:.3f}")

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Node error: {e}")
    finally:
        # Clean shutdown
        if sync_task:
            sync_task.cancel()
        if gossip_task:
            gossip_task.cancel()
        await node.stop()
        logger.info("Node stopped")


async def run_test_network():
    """
    Run a test network with multiple nodes.
    """
    # Create mock chain and mempool
    from ..blockchain.chain import Blockchain
    chain = Blockchain()

    # Start multiple nodes
    nodes = []
    base_port = 8333

    # Start first node
    node1 = Node(chain=chain, host='127.0.0.1', port=base_port)
    await node1.start()
    nodes.append(node1)
    logger.info(f"Started node 1 on port {base_port}")

    # Start additional nodes and connect to first
    for i in range(2, 4):
        port = base_port + i
        node = Node(chain=chain, host='127.0.0.1', port=port)
        await node.start()
        nodes.append(node)

        # Connect to first node
        await node.connect('127.0.0.1', base_port)
        logger.info(f"Started node {i} on port {port}")

    # Let them run
    logger.info(f"Test network running with {len(nodes)} nodes")
    logger.info("Press Ctrl+C to stop")

    try:
        while True:
            await asyncio.sleep(10)

            # Show network status
            for i, node in enumerate(nodes, 1):
                peer_count = node.get_peer_count()
                logger.info(f"Node {i}: {peer_count} peers")

    except KeyboardInterrupt:
        logger.info("Stopping test network...")
    finally:
        for node in nodes:
            await node.stop()


def main():
    """
    Main entry point for network runner.
    """
    parser = argparse.ArgumentParser(description='Run BloomCoin network node')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='Port to listen on')
    parser.add_argument('--seeds', nargs='*', help='Seed nodes (host:port)')
    parser.add_argument('--test', action='store_true', help='Run test network')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.test:
        # Run test network
        asyncio.run(run_test_network())
    else:
        # Parse seed nodes
        seeds = []
        if args.seeds:
            for seed in args.seeds:
                try:
                    host, port = seed.split(':')
                    seeds.append((host, int(port)))
                except ValueError:
                    logger.error(f"Invalid seed format: {seed}")
                    sys.exit(1)

        # Create blockchain and mempool
        try:
            from ..blockchain.chain import Blockchain
            from ..blockchain.mempool import Mempool
            chain = Blockchain()
            mempool = Mempool()
        except ImportError:
            logger.warning("Blockchain not available, running without chain")
            chain = None
            mempool = None

        # Run node
        asyncio.run(run_node(
            host=args.host,
            port=args.port,
            seeds=seeds,
            chain=chain,
            mempool=mempool
        ))


if __name__ == '__main__':
    main()