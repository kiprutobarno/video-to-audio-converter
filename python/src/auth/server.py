import jwt
import datetime
from flask import Flask, request
from flask_mysqldb import MySQL
from os import environ

app = Flask(__name__)
mysql = MySQL(app)
app.config.from_envvar("APP_SETTINGS")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return "missing credentials", 401

    # check db for username and password
    cursor = mysql.connection.cursor()
    result = cursor.execute(
        "SELECT username, password FROM users WHERE username=%s", [data["username"]]
    )
    if result > 0:
        user_row = cursor.fetchone()
        username = user_row[0]
        password = user_row[1]

        if data["username"] != username or data["password"] != password:
            return "Invalid credentials", 401
        else:
            return createJWT(username, environ.get("SECRET_KEY"), True)
    else:
        return "Invalid credentials", 401


@app.route("/authenticate", methods=["POST"])
def authenticate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "missing credentials", 401
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt,
            environ.get("SECRET_KEY"),
            algorithms=["HS256"],
        )

    except (
        jwt.DecodeError,
        jwt.exceptions.InvalidAlgorithmError,
        jwt.exceptions.ExpiredSignatureError,
        jwt.exceptions.InvalidIssuedAtError,
    ) as error:
        return repr(error), 403

    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(datetime.UTC),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# set env by running export APP_SETTINGS=.env
