import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

transport = ASGITransport(app)

@pytest.mark.asyncio
async def test_health_check():
    """
    Проверяет работоспособность эндпоинта /health.
    """
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_browse_without_rabbitmq(mocker):
    """
    Проверяет эндпоинт /browse.
    """
    mock_connection = mocker.Mock()
    mock_channel = mocker.Mock()
    mocker.patch(
        "app.main.get_rabbitmq_connection",
        return_value=(mock_connection, mock_channel)
    )
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/browse", json={"url": "http://example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "URL added to queue"}

@pytest.mark.asyncio
async def test_browse_invalid_url():
    """
    Проверяет обработку невалидного URL в эндпоинте /browse.
    """
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/browse", json={"url": "invalid_url"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Invalid URL"
