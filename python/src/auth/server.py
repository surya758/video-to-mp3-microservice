import os
import datetime
import jwt
from flask import Flask, request
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
mysql = MySQL(app)
bcrypt = Bcrypt(app)

# config
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))
app.config["DEBUG"] = True


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    if not (email and password):
        return "Missing credentials", 401
    # Check if user exists in the database
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT email, password FROM user WHERE email=%s", (email,))

    if res > 0:
        user_row = cur.fetchone()
        email_from_db = user_row[0]
        password_from_db = user_row[1]
        if email != email_from_db or password != password_from_db:
            return "Invalid credentials", 401
        else:
            return createJWT(email, os.environ.get("JWT_SECRET"), True)
    else:
        return "User doesn't exist", 401


@app.route("/validate", methods=["POST"])
def validate():
    auth_header = request.headers["Authorization"]
    if not auth_header:
        return "Missing credentials", 401

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return "Invalid token format", 401

    jwt_token = parts[1]
    try:
        decoded_jwt = jwt.decode(
            jwt_token, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except Exception as e:
        return f"Not authorized: {str(e)}", 401

    return decoded_jwt, 200


def createJWT(email, secret, authz):
    return jwt.encode(
        {
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "isAdmin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
