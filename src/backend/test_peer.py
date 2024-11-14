import threading
import time

from peer import Peer

def start_peer(peer):
    peer.start()
    print(f"Peer started at {peer.host}:{peer.port}")

def main():
    # Initialize peers
    peer1 = Peer('127.0.0.1', 5000)
    peer2 = Peer('127.0.0.1', 5001)
    peer3 = Peer('127.0.0.1', 5002)

    # Start peers in separate threads
    threading.Thread(target=start_peer, args=(peer1,), daemon=True).start()
    threading.Thread(target=start_peer, args=(peer2,), daemon=True).start()
    threading.Thread(target=start_peer, args=(peer3,), daemon=True).start()

    time.sleep(1)

    # Connect peers
    peer1.peers.append(('127.0.0.1', 5001))
    peer1.peers.append(('127.0.0.1', 5002))
    peer2.peers.append(('127.0.0.1', 5000))
    peer2.peers.append(('127.0.0.1', 5002))
    peer3.peers.append(('127.0.0.1', 5000))
    peer3.peers.append(('127.0.0.1', 5001))

    # Send messages
    peer1.send_message("Hello from Peer 1!")
    peer2.send_message("Hello from Peer 2!")
    peer3.send_message("Hello from Peer 3!")



if __name__ == "__main__":
    main()