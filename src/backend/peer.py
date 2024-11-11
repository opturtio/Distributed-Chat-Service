import time
import threading

class Peer:
    def __init__(self, host, port):
        # Initialize a peer node with its host and port information
        self.host = host
        self.port = port
        self.peers = []  # List of connected peers
        self.chat_history = []
        self.message_queue = []  # Queue for undelivered messages
        self.retry_interval = 5  # Retry every 5 seconds

    def start(self):
        # Starts separate threads for listening to peers and retrying unsent messages
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
        threading.Thread(target=self.retry_unsent_messages, daemon=True).start()

    def send_message(self, message):
        # Sends a message to all connected peers
        timestamp = time.time()
        msg = {"timestamp": timestamp, "sender": self.host, "message": message}
        self.chat_history.append(msg)
        self.broadcast_message(msg)

    def broadcast_message(self, message):
        # Attempts to send the message to each peer in the peer list
        for peer in self.peers:
            try:
                self._send_to_peer(peer, message)
            except socket.error:
                print(f"Failed to send to {peer}, adding to queue")
                self.message_queue.append((peer, message))

    def _send_to_peer(self, peer, message):
        # Handles the actual sending of messages to a specified peer
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(peer)
            s.sendall(json.dumps(message).encode())

    def retry_unsent_messages(self):
        # Periodically retries sending messages in the message queue
        while True:
            time.sleep(self.retry_interval)
            for peer, message in self.message_queue[:]:
                try:
                    self._send_to_peer(peer, message)
                    self.message_queue.remove((peer, message))  # Remove on success
                    print(f"Resent message to {peer}")
                except socket.error:
                    print(f"Retry failed for {peer}")
