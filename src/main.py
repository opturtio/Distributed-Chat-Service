import time
import os
from backend.peer import Peer
from backend.connection_manager import received_messages
from dotenv import load_dotenv

load_dotenv()


def console_menu(peer):
    """Provides a console-based menu for user interaction.

    Args:
        peer (Peer): The peer instance managing network communication.
    """
    messages = []
    user_name = input("Enter username: ")
    
    while True:
        print("\nOptions:")
        print("1. Send a message")
        print("2. View messages")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            messages = send_message_cli(peer, user_name, messages)
        elif choice == "2":
            messages = view_messages_cli(messages)
            messages = sorted(messages, key=lambda x: x['timestamp'])
            print("\nMessages:")
            for message in messages:
                print(f"{message['sender']}: {message['message']}")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

def send_message_cli(peer, user_name, messages):
    """Sends a message via the command line interface.

    Args:
        peer (Peer): The peer instance managing network communication.
        user_name (str): The name of the user sending the message.
        messages (list): The list of sent and received messages.
    
    Returns:
        messages (list): The updated list of messages.
    """
    message_content = input("Enter your message: ")
    message = {"timestamp": time.time(), "sender": user_name, "message": message_content}
    peer.send_message(message)
    messages.append(message)
    if len(messages) > 10:
        messages.pop(0)
    return messages

def view_messages_cli(messages):
    """Displays messages received from other peers.
    
    Args:
        messages (list): The list of sent and received messages.
    
    Returns:
        messages (list): The updated list of messages.
    """
    while not received_messages.empty():
        message = received_messages.get()
        messages.append(message)
        if len(messages) > 10:
            messages.pop(0)
    return messages

if __name__ == "__main__":
    peer = Peer("0.0.0.0", os.getenv("peer_info")[1])
    peer.start()
    console_menu(peer)
