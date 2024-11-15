from unittest import mock
from app.consumer import consume


def test_consume(mocker):
    """
    Проверяет работу функции consume и эмуляцию RabbitMQ подключения.
    """
    mock_channel = mocker.Mock()
    mocker.patch(
        "app.consumer.get_rabbitmq_connection", return_value=(None, mock_channel)
    )
    mock_channel.start_consuming = mock.Mock()

    consume()

    mock_channel.start_consuming.assert_called_once()
