from app import app

def test_homepage_works():
    """Test if homepage loads"""
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Weather' in response.data  # Change 'Weather' to match your page