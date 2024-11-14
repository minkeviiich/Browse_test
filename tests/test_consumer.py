import unittest
import json
from unittest.mock import patch, MagicMock
from browse_test.consumer import get_rabbitmq_connection, consume

class TestRabbitMQConnection(unittest.TestCase):
    @patch('pika.BlockingConnection')
    def test_get_rabbitmq_connection(self, MockBlockingConnection):
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        MockBlockingConnection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        connection, channel = get_rabbitmq_connection()

        mock_connection.channel.assert_called_once()
        channel.queue_declare.assert_called_with(queue='url_queue')
        self.assertEqual(connection, mock_connection)
        self.assertEqual(channel, mock_channel)

class TestConsumer(unittest.TestCase):
    @patch('browse_test.consumer.webdriver.Remote')
    @patch('browse_test.consumer.get_rabbitmq_connection')
    def test_callback(self, mock_get_rabbitmq_connection, MockWebDriver):
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_get_rabbitmq_connection.return_value = (mock_connection, mock_channel)

        mock_driver = MagicMock()
        MockWebDriver.return_value = mock_driver

        consume()

        # Simulate message received
        callback_func = mock_channel.basic_consume.call_args[1]['on_message_callback']
        body = json.dumps({"url": "http://example.com"}).encode()
        callback_func(None, None, None, body)

        mock_driver.get.assert_called_once_with("http://example.com")
        mock_driver.quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
