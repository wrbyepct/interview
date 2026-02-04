from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException, status
import torch
from torchvision import transforms
from PIL import Image
from io import BytesIO

from app.model import CNNTransformer
from app.schemas import PredictionResponse, HealthResponse


# Global model storage
ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model at startup, clean up at shutdown"""
    # Startup: Load model once per worker
    model = CNNTransformer()
    model.load_state_dict(torch.load('model_weights.pth', map_location='cpu'))
    model.eval()
    ml_models["mnist"] = model
    print("Model loaded successfully")
    yield
    # Shutdown: Clean up
    ml_models.clear()
    print("Model cleaned up")


app = FastAPI(
    title="MNIST Digit Recognition API",
    description="Upload an image to predict the digit (0-9)",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for container health monitoring"""
    return HealthResponse(status="ok")


@app.post("/predict", response_model=PredictionResponse)
async def predict_digit(file: UploadFile = File(...)):
    """
    Predict digit from uploaded image.

    Args:
        file: Image file (JPEG or PNG)

    Returns:
        PredictionResponse with digit (0-9) and confidence score
    """
    # Validate content type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Only JPEG and PNG are supported."
        )

    try:
        # Read and process image
        content = await file.read()
        img = Image.open(BytesIO(content)).convert("L")  # Convert to grayscale

        # Preprocess image for model
        transform = transforms.Compose([
            transforms.Resize((28, 28)),
            transforms.ToTensor(),
        ])
        img_tensor = transform(img).unsqueeze(0)  # Add batch dimension

        # Run inference
        with torch.inference_mode():
            output = ml_models["mnist"](img_tensor)
            pred = torch.argmax(output, dim=1).item()
            confidence = torch.softmax(output, dim=1).max().item()

        return PredictionResponse(digit=pred, confidence=confidence)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing image: {str(e)}"
        )
