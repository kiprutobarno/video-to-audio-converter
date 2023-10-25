import pika
import json


def upload(file, fs, channel, access):
    # save the file in mongoDB
    try:
        file_id = fs.put(file)
    except Exception as err:
        return "internal server error", 500
    # create the message
    message = {"video_id": str(file_id), "mp3_id": None, "username": access["username"]}
    # put the message on the RabbitMQ queue
    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    except Exception:
        fs.delete(file_id)
        return "internal server error", 500
