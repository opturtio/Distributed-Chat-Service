from os import getenv
from flask import Flask
from backend.main import main

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.secret_key = getenv("SECRET_KEY")
main()

from backend import routes # noqa: E402, F401

if __name__ == "__main__":
    app.run(debug=True)
