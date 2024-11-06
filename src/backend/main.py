from peer import Peer

def main():
    """Initializes the peer"""
    
    peer = Peer("localhost", 5000)
    peer.start()

if __name__ == "__main__":
    main()
