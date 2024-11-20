import time
from backend.database import insert_message

class MessageManager:
    def __init__(self, connection_manager, logger):
        self.connection_manager = connection_manager
        self.message_queue = []
        self.retry_interval = 1
        self.logger = logger

    def broadcast_message(self, message):
        # Adds a timestamp and sends the message to all peers
        peers = self.connection_manager.peers
        insert_message(message) # Have to figure out best place for this
        self.logger.info(f"Broadcasting message: {message}")
        for peer in peers:
            try:
                self.connection_manager.send_to_peer(peer, message)
            except Exception:
                self.logger.warning(f"Failed to send to {peer}. Adding to queue.")
                self.message_queue.append((peer, message))

    def retry_unsent_messages(self):
        # Retries sending messages in the queue periodically
        while True:
            time.sleep(self.retry_interval)
            for peer, message in self.message_queue[:]:
                try:
                    self._send_to_peer(peer, message)
                    self.message_queue.remove((peer, message))  # Remove on success
                    self.logger.info(f"Successfully resent message to {peer}")
                except Exception:
                    self.logger.warning(f"Retry failed for {peer}")
