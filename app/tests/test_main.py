from fastapi.routing import APIRouter
from fastapi.testclient import TestClient
from fastapi import status

test_router = APIRouter()

@test_router.get("/healthy")
def test_healthy():
    return {'status': 'healthy'}


client = TestClient(test_router)

def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'healthy'}