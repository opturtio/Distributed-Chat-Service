from flask import request, jsonify, render_template
from app import app
from logger import logger
from backend.create_peer import create_peer
import time

peer = create_peer()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    """API endpoint to send a message from the frontend."""
    data = request.json
    message = {
        "timestamp": data.get("timestamp"),
        "sender": data.get("sender"),
        "message": data.get("message"),
    }
    peer.send_message(message)
    logger.info("routes.py: Message sent!")
    return jsonify({"status": "Message sent", "message": message}), 200
