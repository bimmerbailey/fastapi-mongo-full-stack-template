import pytest

from app.models import Item


@pytest.mark.anyio
async def test_create_item(authorized_admin_client, db):
    res = await authorized_admin_client.post(
        "/api/v1/items", json=dict(name="test", cost=100, description="Hello", quantity=4)
    )
    assert res.status_code == 201

    item_query = Item.find({})
    assert await item_query.count() == 1
