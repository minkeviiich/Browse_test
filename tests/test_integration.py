import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from browse_test.main import app
from browse_test.consumer import consume
import pika
import json
import threading
import logging
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegrationTest(unittest.TestCase):
    @patch('browse_test.consumer.webdriver.Remote')
    @patch('pika.BlockingConnection')
    def test_add_url_and_process(self, MockBlockingConnection, MockWebDriver):
        # Настройка клиента FastAPI
        client = TestClient(app)
        
        # Мокинг RabbitMQ
        mock_connection = MagicMock()
        mock_channel = MagicMock()
        MockBlockingConnection.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel

        # Мокинг Selenium
        mock_driver = MagicMock()
        MockWebDriver.return_value = mock_driver
        
        # Запуск потребителя в отдельном потоке
        def run_consumer():
            logger.info("Starting consumer thread")
            consume()
        
        consumer_thread = threading.Thread(target=run_consumer)
        consumer_thread.start()
        
        # Отправка запроса на добавление URL
        logger.info("Sending POST request to /browse endpoint")
        response = client.post("/browse", json={"url": "http://example.com"})
        logger.info(f"Received response: {response.status_code} - {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "URL added to queue"})
        
        # Ожидание обработки сообщения с проверкой
        for _ in range(20):  # Увеличим количество попыток и паузу
            logger.info(f"Checking if URL is processed: {mock_driver.get.call_count} calls made")
            if mock_driver.get.call_count > 0:
                break
            time.sleep(1)
        
        # Проверка обработки URL
        mock_driver.get.assert_called_with("http://example.com")
        mock_driver.quit.assert_called_once()
        
        # Завершение работы потребителя
        consumer_thread.join(timeout=1)
        if consumer_thread.is_alive():
            # Закрытие потока, если он все еще активен
            logger.info("Consumer thread still alive, attempting to close connection")
            mock_connection.close()

if __name__ == '__main__':
    unittest.main()
