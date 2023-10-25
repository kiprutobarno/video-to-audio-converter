import os
import gridfs
import pika
import json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import authenticate
from auth_service import access
from storage import util

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@app.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err


@app.route("/upload", methods=["POST"])
def upload():
    access, err = authenticate.token(request)
    access = json.loads(access)
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly one file is required", 400
        for _, file in request.files.items():
            err = util.upload(file, fs, channel, access)
            if err:
                return err
        return "Success", 200
    else:
        return "Not enough privileges", 403


@app.route("/download", methods=["GET"])
def download():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
