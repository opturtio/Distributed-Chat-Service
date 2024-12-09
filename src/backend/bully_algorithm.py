import threading
import time
from logger import logger

class BullyAlgorithm:
    def __init__(self, node_id, peers, connection_manager):
        self.node_id = node_id
        self.priority = 1
        self.peers = peers
        self.leader = None
        self.peer_priorities = {}
        self.connection_manager = connection_manager
        self.update_peer_priorities()
    
    def update_peer_priorities(self):
        """Contacts peers and increases their priority."""
        logger.info("bully_algorithm/update_peer_priorities: Updating peer priorities...")
        self.connection_manager.contact_peers_and_increase_priority()
        logger.info("bully_algorithm/update_peer_priorities: Peer priorities updated.")
        logger.info("Your current priority is {self.priority}")

    
    def check_leader(self):
        # Periodically check if the leader is reachable
        if not self.ping_leader():
            self.start_election()

    def ping_leader(self):
        # Simulate a ping to the leader (e.g., using a socket or message)
        try:
            # Ping logic here
            pass
        except:
            return False
    
    def start_election(self):
        higher_priority_peers = [peer for peer in self.peers if peer.priority > self.priority]

        if not higher_priority_peers:
            # If no higher-priority peers exist, declare self as leader
            self.declare_leader()
        else:
            # Notify higher-priority peers
            responses = []
            for peer in higher_priority_peers:
                responses.append(self.send_election_message(peer))

            # Wait for responses
            if any(responses):
                pass
            else:
                self.declare_leader()

    def send_election_message(self, peer):
        # Simulate sending an election message
        pass

    def declare_leader(self):
        self.leader = self.node_id
        self.announce_leader()

    def announce_leader(self):
        pass

    def receive_leader_announcement(self, leader_id):
        self.leader = leader_id
