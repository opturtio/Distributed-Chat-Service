import threading

class LeaderManager:

    def __init__(self, node_id, connection_manager, message_manager):
        """
        Manages leader status.
        
        Args:
            node_id (str): The ID of the current node.
            connection_manager (ConnectionManager): The connection manager for peer communication.
        """
        self.node_id = node_id
        self.connection_manager = connection_manager
        self.message_manager = message_manager
        self.message_queue = message_manager.message_queue
        self.is_leader = False 
        self.processed_messages = []

    def declare_leader(self):
        """Declare the current node as the leader and announce to peers."""
        self.is_leader = True
        message = {"type": "leader_announcement", "leader_id": self.node_id}
        self.message_manager.broadcast_message(message)
        threading.Thread(target=self.manage_messages, daemon=True).start()

    def handle_leader_announcement(self, leader_id):
        """Update the leader based on an announcement."""
        self.is_leader = leader_id == self.node_id
        self.connection_manager.set_leader(leader_id)

    def ping_leader(self):
        """Respond to ping requests."""
        return {"status": "alive"}
