import socket
import threading
import json
from app import socketio
from backend.database import insert_message

class ConnectionManager:
    def __init__(self, host, port, peers, logger):
        self.host = host
        self.port = port
        self.peers = peers
        self.logger = logger

    def listen_for_peers(self):
        """ Listens for incoming connections from other peers """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            self.logger.info(f"Listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_peer, args=(conn, addr), daemon=True).start()

    def handle_peer(self, conn, addr):
        """ Handles incoming messages from a peer """
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                self.logger.info(f"Received message from {message['sender']}: {message['message']}")
                
                # Insert message into the database
                insert_message(message)
                
                # Emit the message to all connected WebSocket clients
                self.logger.info("Broadcasting to WebSocket clients") 
                socketio.emit("new_message", message, broadcast=True)

    def send_to_peer(self, peer, message):
        """ Sends a message to a specific peer """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(peer)
                s.sendall(json.dumps(message).encode())
            self.logger.info(f"Message sent to {peer}")
        except socket.error as e:
            self.logger.error(f"Failed to send message to {peer}: {e}")
            raise
