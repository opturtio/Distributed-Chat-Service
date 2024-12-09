import threading
from backend.connection_manager import ConnectionManager
from backend.message_manager import MessageManager
from backend.leader_manager import LeaderManager
from backend.bully_algorithm import BullyAlgorithm
from logger import logger
import secrets


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
        self.node_id = secrets.token_hex(64)
        self.priority = self.form_priority()
        self.peers = [('127.0.0.1', 6060)]  # Example connected peer
        self.connection_manager = ConnectionManager(self.host, self.port, self.peers)
        self.message_manager = MessageManager(self.connection_manager)
        self.leader_manager = LeaderManager(self.node_id, self.connection_manager, self.message_manager)
        self.bully_algorithm = BullyAlgorithm(self.node_id, self.priority, self.peers)
        logger.info(f"peer/init: Peer initialized with host={host}, port={port}")

    def start(self):
        """Starts the peer's connection listener and message retry threads."""
        logger.info("peer/start: Starting peer services.")
        threading.Thread(target=self.connection_manager.listen_for_peers, daemon=True).start()
        threading.Thread(target=self.message_manager.retry_unsent_messages, daemon=True).start()

    def send_message(self, message):
        """Sends a message to all connected peers.

        Args:
            message (dict): The message to send.
        """
        logger.info(f"peer/send_message: Sending message: {message}")
        self.message_manager.broadcast_message(message)

    def form_priority(self):
        return self.connection_manager.count_peers()