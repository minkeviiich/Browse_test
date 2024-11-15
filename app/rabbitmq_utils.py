import logging
import time
from typing import Any
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika import BlockingConnection


def get_rabbitmq_connection() -> tuple[BlockingConnection, BlockingChannel]:
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
