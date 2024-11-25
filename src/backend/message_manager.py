import time
from logger import logger
from backend.database import insert_message

class MessageManager:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
        self.message_queue = []
        self.retry_interval = 1

    def broadcast_message(self, message):
        # Adds a timestamp and sends the message to all peers
        peers = self.connection_manager.peers
        insert_message(message) # Have to figure out best place for this
        logger.info(f"Broadcasting message: {message}")
        for peer in peers:
            logger.info(f"message_manager broadcast_message: peer {peer}")
            try:
                self.connection_manager.send_to_peer(peer, message)
            except Exception:
                logger.warning(f"Failed to send to {peer}. Adding message to queue.")
                self.message_queue.append((peer, message))

    def retry_unsent_messages(self):
        # Retries sending messages in the queue periodically
        while True:
            time.sleep(self.retry_interval)
            for peer, message in self.message_queue[:]:
                try:
                    self.send_to_peer(peer, message)
                    self.message_queue.remove((peer, message))  # Remove on success
                    logger.info(f"Successfully resent message to {peer}")
                except Exception:
                    logger.warning(f"Retry failed for {peer}")
