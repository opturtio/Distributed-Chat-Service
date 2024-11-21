from flask import render_template
from app import app, socketio
from backend.create_peer import create_peer
from backend.database import insert_message
import time

peer_instance = create_peer()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@socketio.on("send_message")
def handle_send_message(data):
    """
    Handles a message sent from the frontend.
    Broadcasts it to all connected clients (including peers).
    """
    message = {
        "timestamp": time.time(),
        "sender": data["sender"],
        "message": data["message"]
    }

    app.logger.info(f"Broadcasting message: {message}") 
    
    # Insert the message into the database
    insert_message(message)
    print(f"Broadcasting message: {message}")
    # Emit the message to all connected clients
    socketio.emit("new_message", message, broadcast=True)

    # Forward the message to all peers
    peer_instance.send_message(message)
