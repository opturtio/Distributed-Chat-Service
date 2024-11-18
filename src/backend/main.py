import logging
from backend.peer import Peer

def main():
    """Initializes the peer"""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    peer = Peer("localhost", 5010)
    peer.start()
    logger.info(f"Peer started at {peer.host}:{peer.port}")

if __name__ == "__main__":
    main()