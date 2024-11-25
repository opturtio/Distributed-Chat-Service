import socket
import threading
import json
from logger import logger

class ConnectionManager:
    def __init__(self, host, port, peers):
        self.host = host
        self.port = port
        self.peers = peers

    def listen_for_peers(self):
        """Starts a socket server to listen for incoming connections."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            logger.info(f"Listening on {self.host}:{self.port}")
            while True:
                conn, addr = server_socket.accept()
                threading.Thread(target=self.handle_peer, args=(conn, addr), daemon=True).start()

    def handle_peer(self, conn, addr):
        """Handles communication with a connected peer."""
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                logger.info(f"Received message: {message}")
                self.process_message(message)

    def process_message(self, message):
        """Processes an incoming message."""
        logger.info(f"Processing message: {message}")

    def broadcast_message(self, message):
        """Broadcasts a message to all connected peers."""
        for peer in self.peers:
            try:
                self.send_to_peer(peer, message)
            except Exception as e:
                logger.error(f"Failed to send message to {peer}: {e}")

    def send_to_peer(self, peer, message):
        """Sends a message to a specific peer."""
        logger.info(f"connection_manager send_to_peer: Sending message to {peer}: {message}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(5)  # Set a timeout of 10 seconds
                client_socket.connect(peer)
                client_socket.sendall(json.dumps(message).encode())
                logger.info(f"Sent message to {peer}: {message}")
        except socket.timeout:
            logger.error(f"Timeout occurred while trying to connect to {peer}")
        except Exception as e:
            logger.error(f"Failed to send message to {peer}: {e}")