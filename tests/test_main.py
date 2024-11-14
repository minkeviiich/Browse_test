import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from browse_test.main import app, get_rabbitmq_connection

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

class TestBrowseEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('browse_test.main.get_rabbitmq_connection')
    def test_browse(self, mock_get_rabbitmq_connection):
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_get_rabbitmq_connection.return_value = (mock_connection, mock_channel)

        response = self.client.post("/browse", json={"url": "http://example.com"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "URL added to queue"})
        mock_channel.basic_publish.assert_called_once()

if __name__ == '__main__':
    unittest.main()
