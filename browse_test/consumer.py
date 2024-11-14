import logging
import json
from typing import Any
from selenium import webdriver
from rabbitmq_utils import get_rabbitmq_connection

logging.basicConfig(level=logging.INFO)


def consume() -> None:
    """
    Читает сообщения из очереди RabbitMQ и обрабатывает их с использованием Selenium.
    """

    connection, channel = get_rabbitmq_connection()

    def callback(_ch: Any, _method: Any, _properties: Any, body: bytes) -> None:
        """
        Обрабатывает сообщение из очереди RabbitMQ.
        """

        url: str = json.loads(body)["url"]
        logging.info("Processing URL: %s", url)
        try:
            options = webdriver.ChromeOptions()
            driver = webdriver.Remote(
                command_executor="http://selenium-hub:4444/wd/hub", options=options
            )
            logging.info("Browser started successfully")
            driver.get(url)
            page_source: str = driver.page_source
            logging.info(
                "Page source for %s:\n%s", url, page_source[:1000]
            )  # Логирование первых 1000 символов HTML
            driver.quit()
            logging.info("Browser closed successfully")
        except Exception as e:
            logging.error("Error processing URL: %s", e)

    channel.basic_consume(
        queue="url_queue", on_message_callback=callback, auto_ack=True
    )
    logging.info("Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    consume()
