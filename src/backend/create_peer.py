from backend.peer import Peer

def create_peer():
    """Initializes the peer"""
    
    peer = Peer("0.0.0.0", 8080)
    peer.start()

    return peer
