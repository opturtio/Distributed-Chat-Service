import time
from logger import logger

class MessageManager:
    """Handles the broadcasting and retrying of unsent messages."""

    def __init__(self, connection_manager):
        """Initializes the message manager.

        Args:
            connection_manager (ConnectionManager): The connection manager to use for sending messages.
        """
        self.connection_manager = connection_manager
        self.message_queue = []
        self.retry_interval = 1

    def broadcast_message(self, message):
        """Broadcasts a message to all peers.

        Args:
            message (dict): The message to broadcast.
        """
        peers = self.connection_manager.peers
        logger.info(f"message_manager/broadcast_message: Broadcasting message: {message}")
        for peer in peers:
            logger.info(f"message_manager/broadcast_message: peer {peer}")
            try:
                self.connection_manager.send_to_peer(peer, message)
            except Exception:
                logger.warning(f"Failed to send to {peer}. Adding message to queue.")
                self.message_queue.append((peer, message))

    def retry_unsent_messages(self):
        """Retries sending unsent messages periodically."""
        while True:
            time.sleep(self.retry_interval)
            for peer, message in self.message_queue[:]:
                try:
                    self.connection_manager.send_to_peer(peer, message)
                    self.message_queue.remove((peer, message))  # Remove on success
                    logger.info(f"message_manager/retry_unsent_messages: Successfully resent message to {peer}")
                except Exception:
                    logger.warning(f"message_manager/retry_unsent_messages: Retry failed for {peer}")
