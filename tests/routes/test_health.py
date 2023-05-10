from fastapi.testclient import TestClient


def test_health(cli: TestClient):
    resp = cli.get("/api/fastapi-template/health")
    assert resp.status_code == 200
    assert resp.text == "success"
