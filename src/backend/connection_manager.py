import socket
import threading
import json
from logger import logger
from queue import Queue

frontend_message_queue = Queue()

class ConnectionManager:
    """Manages peer-to-peer connections, message handling, and broadcasting."""

    def __init__(self, host, port, peers):
        """Initializes the connection manager.

        Args:
            host (str): The host address for the connection manager.
            port (int): The port number for the connection manager.
            peers (list): A list of connected peers as (host, port) tuples.
        """
        self.host = host
        self.port = port
        self.peers = peers

    def listen_for_peers(self):
        """Starts a socket server to listen for incoming connections."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            logger.info(f"connection_manager/listen_for_peers: Listening on {self.host}:{self.port}")
            while True:
                conn, addr = server_socket.accept()
                logger.info(f"connection_manager/listen_for_peers: Connection accepted from {addr}")
                threading.Thread(target=self.handle_peer, args=(conn, addr), daemon=True).start()

    def handle_peer(self, conn, addr):
        """Handles communication with a connected peer.

        Args:
            conn (socket): The socket connection to the peer.
            addr (tuple): The address of the connected peer.
        """
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                logger.info(f"connection_manager/handle_peer: Received message: {message}")
                self.process_message(message)

    def process_message(self, message):
        """Processes an incoming message.

        Args:
            message (dict): The message received from a peer.
        """
        frontend_message_queue.put(message)
        logger.info(f"connection_manager/process_message: Message added to queue: {message}")
        logger.info(f"connection_manager/process_message: Queue size: {frontend_message_queue.qsize()}")

    def broadcast_message(self, message):
        """Broadcasts a message to all connected peers.

        Args:
            message (dict): The message to broadcast.
        """
        for peer in self.peers:
            try:
                self.send_to_peer(peer, message)
                logger.info(f"connection_manager/broadcast_message: Sent message to {peer}: {message}")
            except Exception as e:
                logger.error(f"connection_manager/broadcast_message: Failed to send message to {peer}: {e}")

    def send_to_peer(self, peer, message):
        """Sends a message to a specific peer.

        Args:
            peer (tuple): The (host, port) of the peer to send the message to.
            message (dict): The message to send.
        """
        logger.info(f"connection_manager/send_to_peer: Sending message to {peer}: {message}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(peer)
                client_socket.sendall(json.dumps(message).encode())
                logger.info(f"connection_manager/send_to_peer: Sent message to {peer}: {message}")
        except Exception as e:
            logger.error(f"connection_manager/send_to_peer: Failed to send message to {peer}: {e}")
