"""
Test script for FastAPI application functionality.
Verifies /health and /predict endpoints work correctly.
"""

from fastapi.testclient import TestClient
from app.main import app


def test_health_endpoint():
    """Test health check endpoint"""
    with TestClient(app) as client:
        resp = client.get('/health')
        assert resp.status_code == 200
        assert resp.json()['status'] == 'ok'
        print('✓ Health check: OK')


def test_predict_endpoint():
    """Test prediction endpoint with sample image"""
    with TestClient(app) as client:
        with open('saved_images/img_0_label_6.png', 'rb') as f:
            resp = client.post('/predict', files={'file': ('test.png', f, 'image/png')})

        assert resp.status_code == 200
        data = resp.json()
        assert 'digit' in data and 'confidence' in data
        assert 0 <= data['digit'] <= 9
        assert 0.0 <= data['confidence'] <= 1.0
        print(f'✓ Predict: digit={data["digit"]}, confidence={data["confidence"]:.4f}')


def test_invalid_file_type():
    """Test that invalid file types are rejected"""
    with TestClient(app) as client:
        resp = client.post('/predict', files={'file': ('test.txt', b'not an image', 'text/plain')})
        assert resp.status_code == 400
        assert 'Invalid file type' in resp.json()['detail']
        print('✓ Invalid file type rejected')


if __name__ == '__main__':
    test_health_endpoint()
    test_predict_endpoint()
    test_invalid_file_type()
    print('✓ All API tests passed!')
