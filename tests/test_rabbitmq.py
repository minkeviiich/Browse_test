import pytest
from unittest import mock
from app.rabbitmq_utils import get_rabbitmq_connection
import pika


def test_get_rabbitmq_connection_success():
    """
    Проверяет успешное подключение к RabbitMQ.
    """
    with mock.patch("pika.BlockingConnection") as MockConnection:
        mock_connection = MockConnection.return_value
        mock_channel = mock_connection.channel.return_value
        connection, channel = get_rabbitmq_connection()
        assert connection == mock_connection
        assert channel == mock_channel


def test_get_rabbitmq_connection_failure():
    """
    Проверяет обработку ошибки подключения к RabbitMQ.
    """
    with mock.patch(
        "pika.BlockingConnection", side_effect=pika.exceptions.AMQPConnectionError
    ):
        with pytest.raises(RuntimeError) as excinfo:
            get_rabbitmq_connection()
        assert str(excinfo.value) == "Failed to connect to RabbitMQ"
