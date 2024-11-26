from flask import request, Response, jsonify, render_template
from app import app
from logger import logger
from backend.create_peer import create_peer
from backend.connection_manager import frontend_message_queue
import time, json

peer = create_peer()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/stream_messages", methods=["GET"])
def stream_messages():
    """Streams messages to the frontend."""
    def stream():
        while True:
            try:
                if not frontend_message_queue.empty():
                    message = frontend_message_queue.get()
                    yield f"data: {json.dumps(message)}\n\n"
                time.sleep(1)
            except Exception as e:
                logger.error(f"stream_messages: Error streaming message: {e}")
                break
    return Response(stream(), content_type="text/event-stream")

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
    logger.info(f"routes/send_message: Message sent {message}!")
    return jsonify({"status": "Message sent", "message": message}), 200
