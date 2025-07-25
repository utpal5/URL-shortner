import pytest
import json
from app.main import app, url_store

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_shorten_url(client):
    response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data

def test_redirect_url(client):
    # First shorten a URL
    response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    short_code = response.get_json()["short_code"]

    # Test redirect
    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.location == "https://www.example.com"

def test_get_stats(client):
    # Shorten a URL
    response = client.post('/api/shorten', json={"url": "https://www.example.com"})
    short_code = response.get_json()["short_code"]

    # Access redirect to increment clicks
    client.get(f'/{short_code}')

    # Get stats
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["url"] == "https://www.example.com"
    assert data["clicks"] == 1
    assert "created_at" in data

def test_invalid_url(client):
    response = client.post('/api/shorten', json={"url": "invalid-url"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_nonexistent_short_code(client):
    response = client.get('/api/stats/nonexistent')
    assert response.status_code == 404

def test_concurrent_shorten_and_redirect(client):
    import concurrent.futures

    urls = [f"https://example.com/page{i}" for i in range(10)]
    short_codes = []

    def shorten(url):
        resp = client.post('/api/shorten', json={"url": url})
        assert resp.status_code == 200
        return resp.get_json()["short_code"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(shorten, urls))
        short_codes.extend(results)

    def redirect(short_code):
        resp = client.get(f'/{short_code}')
        assert resp.status_code == 302

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        list(executor.map(redirect, short_codes))

def test_edge_case_urls(client):
    valid_urls = [
        "http://localhost",
        "https://127.0.0.1",
        "https://sub.domain.example.com",
        "https://example.com:8080/path?query=string#fragment",
        "https://example.com/~user",
    ]
    for url in valid_urls:
        resp = client.post('/api/shorten', json={"url": url})
        assert resp.status_code == 200

def test_malformed_requests(client):
    # Missing JSON body
    resp = client.post('/api/shorten')
    assert resp.status_code == 400

    # Invalid JSON
    resp = client.post('/api/shorten', data="notjson", content_type='application/json')
    assert resp.status_code == 400

    # JSON without 'url' key
    resp = client.post('/api/shorten', json={"wrong_key": "value"})
    assert resp.status_code == 400
