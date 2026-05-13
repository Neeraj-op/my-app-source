import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Test the main / endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['status'] == 'success'

def test_health_endpoint(client):
    """Test the /health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_missing_endpoint(client):
    """Test accessing non-existent endpoint"""
    response = client.get('/non-existent')
    assert response.status_code == 404