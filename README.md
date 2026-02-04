# MNIST Digit Recognition API

A production-ready REST API for handwritten digit recognition (0-9) powered by a CNN-Transformer neural network. Built with FastAPI and PyTorch, this service accepts images of any size and returns predictions with confidence scores.

![Python 3.13](https://img.shields.io/badge/python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-green)
![Docker Ready](https://img.shields.io/badge/docker-ready-blue)

## Quick Start

Get your first prediction in 30 seconds:

```bash
# Build the Docker image
docker build -t mnist-api .

# Run the container
docker run -d -p 8000:8000 --name mnist mnist-api

# Test prediction with example image
curl -X POST http://localhost:8000/predict \
  -F "file=@saved_images/img_0_label_6.png"
```

Expected response:
```json
{"digit": 6, "confidence": 0.9823}
```

## Features

- **Digit Recognition**: Predicts handwritten digits from 0-9
- **Confidence Scores**: Returns prediction confidence (0.0-1.0)
- **Flexible Input**: Accepts JPEG and PNG images of any size
- **Auto-Processing**: Automatically resizes and converts images to 28x28 grayscale
- **Docker Containerized**: Easy deployment with built-in health checks
- **Concurrent Support**: Handles multiple simultaneous requests
- **Production Ready**: Non-root user, proper signal handling, health monitoring

## Installation

### Docker (Recommended)

```bash
# Build the image
docker build -t mnist-api .

# Run the container
docker run -d -p 8000:8000 --name mnist mnist-api

# Verify health
curl http://localhost:8000/health
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
fastapi run app/main.py --port 8000
```

Note: Requires Python 3.13+ and model_weights.pth in the project root.

## Usage

### Predict Digit from Image

**Using curl:**

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@/path/to/your/image.png"
```

Example response:
```json
{
  "digit": 7,
  "confidence": 0.9912
}
```

**Using Python requests:**

```python
import requests

# Predict from file
with open('digit_image.png', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f}
    )

result = response.json()
print(f"Predicted digit: {result['digit']}")
print(f"Confidence: {result['confidence']:.4f}")
```

**Using Python with image URL:**

```python
import requests
from io import BytesIO

# Download image from URL
image_url = 'https://example.com/digit.jpg'
image_data = requests.get(image_url).content

# Send to API
response = requests.post(
    'http://localhost:8000/predict',
    files={'file': ('image.jpg', BytesIO(image_data), 'image/jpeg')}
)

result = response.json()
print(f"Digit: {result['digit']}, Confidence: {result['confidence']:.2%}")
```

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{"status": "ok"}
```

## API Reference

### POST /predict

Predict the digit from an uploaded image.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (form field) - Image file (JPEG or PNG)

**Response:**
```json
{
  "digit": 6,
  "confidence": 0.9823
}
```

**Fields:**
- `digit` (integer): Predicted digit, range 0-9
- `confidence` (float): Prediction confidence score, range 0.0-1.0

**Supported Image Formats:**
- JPEG (image/jpeg)
- PNG (image/png)

**Image Processing:**
- Any input size accepted
- Automatically resized to 28x28 pixels
- Automatically converted to grayscale
- Normalized for model input

**Error Responses:**

400 Bad Request - Invalid file type:
```json
{
  "detail": "Invalid file type: image/gif. Only JPEG and PNG are supported."
}
```

400 Bad Request - Image processing error:
```json
{
  "detail": "Error processing image: [error message]"
}
```

### GET /health

Check service health status.

**Request:**
- Method: `GET`
- No parameters required

**Response:**
```json
{"status": "ok"}
```

**Use Cases:**
- Container health checks
- Load balancer health probes
- Service monitoring

## Model Information

### Architecture

The API uses a CNN-Transformer hybrid architecture for digit recognition:

- **Convolutional Layers**: 2 CNN layers for feature extraction
  - Conv1: 1 → 32 channels, 3x3 kernel
  - Conv2: 32 → 64 channels, 3x3 kernel
  - MaxPooling after each layer
- **Transformer Encoder**: Attention mechanism for pattern recognition
  - 4 attention heads
  - 2 encoder layers
  - Dimension: 128
- **Classification Head**: Fully connected layers
  - Final output: 10 classes (digits 0-9)

### Input Specifications

- **Input Format**: 28x28 grayscale images
- **Preprocessing**:
  - Auto-resize from any input dimension
  - Auto-convert to grayscale
  - Tensor normalization
- **Output**: Digit prediction (0-9) with softmax confidence

### Model Performance

- Trained on MNIST dataset
- Inference time: ~50-100ms per image (CPU)
- Model size: ~2MB (model_weights.pth)

## Docker

### Build Image

```bash
docker build -t mnist-api .
```

Image details:
- Base: python:3.13-slim
- Size: ~1.59GB
- Non-root user: appuser (uid 1000)
- Port: 8000

### Run Container

```bash
# Run in detached mode
docker run -d -p 8000:8000 --name mnist mnist-api

# Run with custom name and port
docker run -d -p 9000:8000 --name my-mnist-api mnist-api
```

### Health Check

The container includes automatic health monitoring:

```bash
# Check container health status
docker ps

# View health check logs
docker inspect --format='{{json .State.Health}}' mnist | python -m json.tool
```

Health check configuration:
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3
- Start period: 40 seconds (allows model loading)

### Container Management

```bash
# View logs
docker logs mnist

# Stop container
docker stop mnist

# Remove container
docker rm mnist

# View resource usage
docker stats mnist
```

### Access API Documentation

Once running, visit:
- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── model.py         # CNN-Transformer model architecture
│   └── schemas.py       # Pydantic response models
├── saved_images/        # Example test images
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
├── model_weights.pth    # Trained model weights
└── README.md           # This file
```

## Testing

Example test images are provided in the `saved_images/` directory:

```bash
# Test with provided examples
for img in saved_images/*.png; do
    echo "Testing: $img"
    curl -X POST http://localhost:8000/predict -F "file=@$img"
    echo ""
done
```

For comprehensive API testing, see the Postman collection in `postman/MNIST_API_Collection.json`.

## Troubleshooting

**Container fails to start:**
- Check Docker logs: `docker logs mnist`
- Verify model_weights.pth exists in build context
- Ensure port 8000 is not already in use

**Health check failing:**
- Wait 40 seconds after startup for model loading
- Check logs for errors: `docker logs mnist`
- Verify health endpoint manually: `curl http://localhost:8000/health`

**Prediction errors:**
- Verify image format is JPEG or PNG
- Check image file is not corrupted
- Review error message in API response

**Performance issues:**
- Container uses CPU inference (PyTorch CPU version)
- Expected latency: 50-100ms per prediction
- For GPU acceleration, modify requirements.txt and Dockerfile

## Technical Details

### Dependencies

Core dependencies (see requirements.txt for versions):
- fastapi[standard]>=0.115.0 - Web framework and server
- torch (CPU version) - Neural network inference
- torchvision - Image transformations
- Pillow - Image processing
- pydantic>=2.0.0 - Data validation

### Performance

- Startup time: ~30-40 seconds (model loading)
- Prediction latency: 50-100ms (CPU inference)
- Memory usage: ~500MB per container
- Concurrent requests: Supported via Uvicorn workers

### Security

- Runs as non-root user (appuser, uid 1000)
- Input validation on content types
- Error handling for malformed images
- No persistent data storage
- Stateless design for horizontal scaling

## License

This project is part of a technical assessment.
