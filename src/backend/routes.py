from flask import render_template, jsonify, request, redirect
from app import app
from backend.create_peer import create_peer

peer_instance = create_peer()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        message = request.form["message"]
        peer_instance.send_message(message)
        return redirect("/")
