import json
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, field_validator, FieldValidationInfo, ValidationError 
import validators
from browse_test.rabbitmq_utils import get_rabbitmq_connection

app = FastAPI()


class UrlRequest(BaseModel):
    """
    Класс для обработки запросов URL.
    """

    url: str

    @field_validator('url')
    def validate_url(cls, value: str, info: FieldValidationInfo) -> str:
        if not validators.url(value):
            raise ValueError('Invalid URL')
        return value


@app.post("/browse")
def browse(url_request: UrlRequest) -> dict:
    """
    Обрабатывает POST-запрос
    и отправляет URL в очередь RabbitMQ.
    """
    try:
        connection, channel = get_rabbitmq_connection()
        message: str = json.dumps({"url": url_request.url})
        channel.basic_publish(exchange="", routing_key="url_queue", body=message)
        connection.close()
        return {"message": "URL added to queue"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
