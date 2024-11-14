import unittest
from fastapi.testclient import TestClient
from browse_test.main import app
from unittest.mock import patch, MagicMock
from browse_test.rabbitmq_utils import get_rabbitmq_connection

client = TestClient(app)

class TestMain(unittest.TestCase):
    """
    Тесты для main.py.
    """

    @patch("browse_test.main.get_rabbitmq_connection")
    def test_browse_success(self, mock_get_rabbitmq_connection):
        """
        Проверяет успешный POST запрос к /browse.
        """
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        mock_get_rabbitmq_connection.return_value = (mock_connection, mock_channel)

        response = client.post("/browse", json={"url": "http://example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "URL added to queue"})
        mock_channel.basic_publish.assert_called_once()

    @patch("browse_test.main.get_rabbitmq_connection", side_effect=Exception("Connection error"))
    def test_browse_failure(self, mock_get_rabbitmq_connection):
        """
        Проверяет неудачный POST запрос к /browse.
        """
        response = client.post("/browse", json={"url": "http://example.com"})
        self.assertEqual(response.status_code, 500)
        self.assertIn("detail", response.json())

    def test_validate_url(self):
        """
        Проверяет валидацию URL.
        """
        response = client.post("/browse", json={"url": "invalid-url"})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
