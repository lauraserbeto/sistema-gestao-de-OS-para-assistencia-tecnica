from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_stock_cannot_be_negative():
    response = client.post(
        "/estoque/saida",
        json={
            "peca_id": 1,
            "quantidade": 999999
        }
    )

    assert response.status_code in [400, 422]