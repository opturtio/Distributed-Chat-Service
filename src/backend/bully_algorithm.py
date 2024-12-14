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
        self.find_leader()
    
    def update_peer_priorities(self):
        """Contacts peers and increases their priority."""
        print("bully_algorithm/update_peer_priorities: Updating peer priorities...")
        print("bully_algorithm/update_peer_priorities: current priority in bully is", self.priority)
        self.connection_manager.contact_peers_and_increase_priority()
        self.priority = self.connection_manager.fetch_priority()
        print("bully_algorithm/update_peer_priorities: Peer priorities updated.")
        print(f"bully_algorithm/update_peer_priorities: Your current priority is {self.priority}")

    def find_leader(self):
        print("bully_algorithm/find_leader: Finding leader...")
        found = self.connection_manager.find_leader()
        if found:
            if found[1]:
                self.leader = found[0]
                print(f"bully_algorithm/find_leader: Found leader, leader is {self.leader}")    
        else:
            self.leader = self.node_id
            print("bully_algorithm/find_leader: Failed to find leader. Assigning self as leader.")
        

    
    def check_leader(self):
        # Periodically check if the leader is reachable
        if not self.ping_leader():
            self.start_election()

    def ping_leader(self):
        # Simulate a ping to the leader (e.g., using a socket or message)
        try:
            self.connection_manager.find_leader()
        except:
            return False
    
    def start_election(self):
        higher_priority_peers = [peer for peer in self.peers if self.connection_manager.find_priority(peer) > self.priority]

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
