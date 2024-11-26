from os import getenv
from flask import Flask

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.secret_key = getenv("SECRET_KEY")

from backend import routes # noqa: E402, F401

if __name__ == "__main__":
    app.run(debug=True, port=6060)