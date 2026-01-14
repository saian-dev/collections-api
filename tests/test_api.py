import pytest


@pytest.mark.asyncio
async def test_get_games(async_client, settings):
    response = await async_client.get("/games/")
    assert response.status_code == 200
