import time
from backend.peer import Peer
from backend.connection_manager import frontend_message_queue

def console_menu(peer):
    """Provides a console-based menu for user interaction.

    Args:
        peer (Peer): The peer instance managing network communication.
    """
    user_name = input("Enter username: ")
    
    while True:
        print("\nOptions:")
        print("1. Send a message")
        print("2. View received messages")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            send_message_cli(peer, user_name)
        elif choice == "2":
            view_messages_cli()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

def send_message_cli(peer, user_name):
    """Sends a message via the command line interface.

    Args:
        peer (Peer): The peer instance managing network communication.
    """
    message = input("Enter your message: ")
    peer.send_message({"timestamp": time.time(), "sender": user_name, "message": message})

def view_messages_cli():
    """Displays messages received from other peers."""
    while not frontend_message_queue.empty():
        message = frontend_message_queue.get()
        print(f"Message from {message['sender']}: {message['message']}")

if __name__ == "__main__":
    peer = Peer("0.0.0.0", 8080)
    peer.start()
    console_menu(peer)
