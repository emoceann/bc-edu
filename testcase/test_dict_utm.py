from ._conftest import *


@pytest.mark.anyio
async def test_register_user(client: AsyncClient):
    response = await client.get("/utm/link", params={
        "utm_source": "Nikita",
        "utm_medium": "Adset_1",
        "utm_campaign": "Conversions_alliance_1",
        "utm_content": 5,
    })
    assert response.is_redirect is True
