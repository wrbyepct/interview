from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """Response model for digit prediction"""
    digit: int = Field(..., ge=0, le=9, description="Predicted digit (0-9)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(default="ok", description="Service status")
