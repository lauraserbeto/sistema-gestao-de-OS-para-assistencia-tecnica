from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_order_cannot_finish_without_technician():
    response = client.patch(
        "/ordens-servico/1/finalizar"
    )

    assert response.status_code in [400, 422]