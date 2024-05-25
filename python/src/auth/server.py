import os
import datetime
import jwt
from flask import Flask, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
mysql = MySQL(app)

# config
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")
app.config["DEBUG"] = True


@app.route("/login", methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]
    if not username or password:
        return "missing credentials", 404

    # Check if user exists in the database


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
