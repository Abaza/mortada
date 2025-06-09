from fastapi.testclient import TestClient
from fastapi_app.main import app

client = TestClient(app)

def test_ask():
    resp = client.post('/ask', json={'query': 'test'}, headers={'X-API-Key': 'dev'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'answer' in data and 'citations' in data
