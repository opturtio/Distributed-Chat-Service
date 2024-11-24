from backend.peer import Peer

def create_peer():
    """Initializes the peer"""
    
    peer = Peer("localhost", 8080)
    peer.start()

    return peer
