import threading
import time
import os
from dotenv import load_dotenv
from backend.connection_manager import ConnectionManager
from backend.message_manager import MessageManager
from backend.bully_algorithm import BullyAlgorithm
from logger import logger
import secrets

load_dotenv()

class Peer:
    """Represents a peer in the P2P network."""

    def __init__(self, host, port):
        """Initializes the peer instance.

        Args:
            host (str): The host address of this peer.
            port (int): The port number of this peer.
        """
        self.host = host
        self.port = port
        self.peers = [(os.getenv("peer_host"), int(os.getenv("peer_port")))]  # Example connected peer
        self.connection_manager = ConnectionManager(self.host, self.port, self.peers, self.node_id)
        self.message_manager = MessageManager(self.connection_manager)
        self.bully_algorithm = BullyAlgorithm(self.peers, self.connection_manager)
        logger.info(f"peer/init: Peer initialized with host={host}, port={port}")

    def start(self):
        """Starts the peer's connection listener and message retry threads."""
        logger.info("peer/start: Starting peer services.")
        self.connection_manager.inform_peer(self.peers[0])
        threading.Thread(target=self.connection_manager.listen_for_peers, daemon=True).start()
        threading.Thread(target=self.message_manager.retry_unsent_messages, daemon=True).start()
        threading.Thread(target=self.leader_check, daemon=True).start()

    def send_message(self, message):
        """Sends a message to all connected peers.

        Args:
            message (dict): The message to send.
        """
        logger.info(f"peer/send_message: Sending message: {message}")
        #self.bully_algorithm.check_leader()
        self.message_manager.broadcast_message(message)

    def report_priority(self):
        """Reports the peer's current priority"""
        return self.bully_algorithm.priority
    
    def leader_check(self):
        """Periodically checks if the leader is reachable and starts an election if not."""
        while True:
            logger.info("peer/periodic_leader_check: Checking if leader is reachable.")
            self.bully_algorithm.check_leader()
            time.sleep(10)  # Check every 10 seconds