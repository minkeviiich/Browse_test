import logging
import json
from typing import Any
from selenium import webdriver
from app.rabbitmq_utils import get_rabbitmq_connection
from app.main import logger


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
        logger.info("Processing URL: %s", url)
        try:
            options = webdriver.ChromeOptions()
            driver = webdriver.Remote(
                command_executor="http://selenium-hub:4444/wd/hub", options=options
            )
            logger.info("Browser started successfully")
            driver.get(url)
            page_source: str = driver.page_source
            logger.info(
                "Page source for %s:\n%s", url, page_source[:1000]
            )  # Логирование первых 1000 символов HTML
            driver.quit()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error("Error processing URL: %s", e)

    channel.basic_consume(
        queue="url_queue", on_message_callback=callback, auto_ack=True
    )
    logger.info("Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    consume()
