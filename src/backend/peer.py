import threading
from backend.connection_manager import ConnectionManager
from backend.message_manager import MessageManager

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
        self.peers = [('127.0.0.1', 6060)]  # Example connected peer
        self.connection_manager = ConnectionManager(self.host, self.port, self.peers)
        self.message_manager = MessageManager(self.connection_manager)

    def start(self):
        """Starts the peer's connection listener and message retry threads."""
        threading.Thread(target=self.connection_manager.listen_for_peers, daemon=True).start()
        threading.Thread(target=self.message_manager.retry_unsent_messages, daemon=True).start()

    def send_message(self, message):
        """Sends a message to all connected peers.

        Args:
            message (dict): The message to send.
        """
        self.message_manager.broadcast_message(message)
