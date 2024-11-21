from os import getenv
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.secret_key = getenv("SECRET_KEY")
socketio = SocketIO(app)

from backend import routes # noqa: E402, F401

if __name__ == "__main__":
    socketio.run(app, debug=True)
