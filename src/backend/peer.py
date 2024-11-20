import threading
import logging
import time
from backend.connection_manager import ConnectionManager
from backend.message_manager import MessageManager

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []  # List of connected peers
        self.logger = self.setup_logger()
        self.connection_manager = ConnectionManager(self.host, self.port, self.peers, self.logger)
        self.message_manager = MessageManager(self.connection_manager, self.logger)

    def setup_logger(self):
        """
        Sets up a logger for the class.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(__name__)

    def start(self):
        """Starts the connection listener and message retry threads"""
        threading.Thread(target=self.connection_manager.listen_for_peers, daemon=True).start()
        threading.Thread(target=self.message_manager.retry_unsent_messages, daemon=True).start()

    def send_message(self, message):
        """Sends a message to all connected peers"""
        timestamp = time.time()
        msg = {"timestamp": timestamp, "sender": self.host, "message": message}
        self.message_manager.broadcast_message(msg)
