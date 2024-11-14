import logging
import time
import os
from typing import Tuple, Any
import pika


def get_rabbitmq_connection() -> Tuple[Any, Any]:
    """
    Настройка подключения к RabbitMQ.
    """

    retries = 5
    while retries:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters('rabbitmq')
            )
            channel = connection.channel()
            channel.queue_declare(queue="url_queue")
            return connection, channel
        except pika.exceptions.AMQPConnectionError:
            logging.error("Connection to RabbitMQ failed, (%d retries left)", retries)
            time.sleep(5)
            retries -= 1
    raise RuntimeError("Failed to connect to RabbitMQ")
