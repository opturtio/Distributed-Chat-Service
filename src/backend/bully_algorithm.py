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
        self.connection_manager.contact_peers_and_increase_priority()
        self.priority = self.connection_manager.fetch_priority()

    def find_leader(self):
        found = self.connection_manager.find_leader()
        if found:
            if found[1]:
                self.leader = found[0] 
                self.connection_manager.is_leader = False
        else:
            print("bully_algorithm/find_leader: No leader found.  it is me then.")
            self.leader = self.node_id
            self.connection_manager.is_leader = True
        

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
        self.priority = self.connection_manager.fetch_priority()
        higher_priority_peers = []

        for peer in self.peers:
            try:
                peer_priority = self.connection_manager.find_priority(peer)
                if peer_priority > self.priority:
                    higher_priority_peers.append(peer)
            except Exception as e:
                pass


        if not higher_priority_peers:
            # If no higher-priority peers exist, declare self as leader
            logger.info("bully_algorithm/start_election: No higher-priority peers found. Declaring self as leader.")
            self.declare_leader()
        else:
            # Notify higher-priority peers
            responses = []
            for peer in higher_priority_peers:
                logger.info(f"bully_algorithm/start_election: Notifying higher-priority peer: {peer}")
                responses.append(self.connection_manager.ping_peer(peer))

            # Wait for responses
            if any(responses):
                logger.info("bully_algorithm/start_election: Higher-priority peer responded. Aborting election.")
                pass
            else:
                self.declare_leader()
                logger.info("bully_algorithm/start_election: No higher-priority peers responded. Declaring self as leader.")


    def declare_leader(self):
        self.leader = self.node_id
        self.announce_leader()

    def announce_leader(self):
        """Announces the leader to all peers."""
        for peer in self.peers:
            try:
                self.connection_manager.announce_leader(peer)
            except Exception as e:
                pass