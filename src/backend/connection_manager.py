import socket
import threading
import json
from logger import logger
from queue import Queue

received_messages = Queue()

class ConnectionManager:
    """Manages peer-to-peer connections, message handling, and broadcasting."""

    def __init__(self, host, port, peers, node_id):
        """Initializes the connection manager.

        Args:
            host (str): The host address for the connection manager.
            port (int): The port number for the connection manager.
            peers (list): A list of connected peers as (host, port) tuples.
        """
        self.node_id = node_id
        self.host = host
        self.port = int(port)
        self.peers = peers
        self.priority = 1
        self.is_leader = False

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
                
                if message.get("type") == "ping":
                    response = {"type": "pong", "status": "alive"}
                    conn.sendall(json.dumps(response).encode())
                    logger.info(f"connection_manager/handle_peer: Sent pong response to {addr}")

                if message.get("type") == "leader_query": 
                    response = {"type": "leader_response", "leader": (self.node_id, self.is_leader)}
                    conn.sendall(json.dumps(response).encode())
                    logger.info(f"connection_manager/handle_peer: Sent leader response to {addr}")
                
                if message.get("type") == "priority_query":
                    response = {"type": "priority_response", "priority": self.priority}
                    conn.sendall(json.dumps(response).encode())
                    logger.info(f"connection_manager/handle_peer: Sent priority response to {addr}")

                if message.get("type") == "leader_announcement":
                    self.is_leader = False
                    logger.info(f"connection_manager/handle_peer: Leader is {message.get('leader')}")

                elif message.get("type") == "increase_priority":
                    self.priority += 1
                    logger.info(f"connection_manager/handle_peer: Increased priority for {addr}: {self.priority}")
                    response = {"type": "priority_updated", "priority": self.priority}
                    conn.sendall(json.dumps(response).encode())

    def process_message(self, message):
        """Processes an incoming message.

        Args:
            message (dict): The message received from a peer.
        """
        received_messages.put(message)
        logger.info(f"connection_manager/process_message: Message added to queue: {message}")
        logger.info(f"connection_manager/process_message: Queue size: {received_messages.qsize()}")

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
            raise
    
    def ping_peer(self, peer):
        """Pings a peer to check if it is alive."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(5)
                client_socket.connect(peer)
                ping_message = {"type": "ping"}
                client_socket.sendall(json.dumps(ping_message).encode())
                logger.info(f"connection_manager/ping_peer: Sent ping to {peer}")

                data = client_socket.recv(1024)
                response = json.loads(data.decode())
                if response.get("status") == "alive":
                    logger.info(f"connection_manager/ping_peer: Peer {peer} is alive")
                    return True
        except Exception as e:
            logger.error(f"connection_manager/ping_peer: Failed to ping peer {peer}: {e}")
        return False
    
    def find_leader(self):
        """Finds the current leader in the network."""
        for peer in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.settimeout(5)
                    client_socket.connect(peer)
                    message = {"type": "leader_query"}
                    client_socket.sendall(json.dumps(message).encode())
                    logger.info(f"connection_manager/find_leader: Sent leader query to {peer}")

                    data = client_socket.recv(1024)
                    response = json.loads(data.decode())

                    if response.get("type") == "leader_response":
                        leader = response.get("leader")
                        logger.info(f"connection_manager/find_leader: Leader is {leader}")
                        return leader
            except Exception as e:
                logger.error(f"connection_manager/find_leader: Failed to query leader from {peer}: {e}")
        return None
    
    def find_priority(self, peer):
        """Finds the current priority of peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(5)
                client_socket.connect(peer)
                message = {"type": "priority_query"}
                client_socket.sendall(json.dumps(message).encode())
                logger.info(f"connection_manager/find_priority: Sent priority query to {peer}")

                data = client_socket.recv(1024)
                response = json.loads(data.decode())

                if response.get("type") == "priority_response":
                    priority = response.get("priority")
                    logger.info(f"connection_manager/find_priority: Priority for {peer} is {priority}")
                    return priority
        except Exception as e:
            logger.error(f"connection_manager/find_priority: Failed to query priority from {peer}: {e}")
        return None

    def send_priority_increment(self, peer):
        """Sends a message to increase the peer's priority."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(peer)
                message = {"type": "increase_priority"}
                client_socket.sendall(json.dumps(message).encode())
                logger.info(f"connection_manager/send_priority_increment: Sent priority increment to {peer}")

                data = client_socket.recv(1024)
                response = json.loads(data.decode())
                logger.info(f"connection_manager/send_priority_increment: Received response from {peer}: {response}")
        except Exception as e:
            logger.error(f"connection_manager/send_priority_increment: Failed to increase priority for peer {peer}: {e}")

    def contact_peers_and_increase_priority(self):
        """Pings all peers and increments their priority if they respond."""
        for peer in self.peers:
            logger.info(f"connection_manager/contact_peers_and_increase_priority: Pinging peer {peer}")
            if self.ping_peer(peer):
                logger.info(f"connection_manager/contact_peers_and_increase_priority: Peer {peer} is alive. Sending priority increment.")
                self.send_priority_increment(peer)
            else:
                logger.warning(f"connection_manager/contact_peers_and_increase_priority: Peer {peer} did not respond.")

    def announce_leader(self, peer):
        """Announces the current leader to peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(peer)
                message = {"type": "leader_announcement", "leader": self.node_id}
                client_socket.sendall(json.dumps(message).encode())
                logger.info(f"connection_manager/announce_leader: Sent leader announcement to {peer}")
        except:
            logger.error(f"connection_manager/announce_leader: Failed to announce leader to {peer}")

    def fetch_priority(self):
        return self.priority