import threading
from backend.connection_manager import ConnectionManager
from backend.message_manager import MessageManager

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.connection_manager = ConnectionManager(self.host, self.port, self.peers)
        self.message_manager = MessageManager(self.connection_manager)

    def start(self):
        """Starts the connection listener and message retry threads"""
        threading.Thread(target=self.connection_manager.listen_for_peers, daemon=True).start()
        threading.Thread(target=self.message_manager.retry_unsent_messages, daemon=True).start()

    def send_message(self, message):
        """Sends a message to all connected peers"""
        self.message_manager.broadcast_message(message)
