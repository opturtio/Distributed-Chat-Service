from backend.peer import Peer

def create_peer():
    """Initializes the peer"""
    
    peer = Peer("localhost", 5010)
    peer.start()
    peer.setup_logger()
    peer.logger.info(f"Peer started at {peer.host}:{peer.port}")

    return peer
