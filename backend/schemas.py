from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime

# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Image Generation Schemas
class ImageCustomization(BaseModel):
    style: str = Field(..., description="Style: minimalist, maximalist, elegant, modern, classic")
    color_scheme: str = Field(..., description="Color scheme: gold, silver, black_gold, rose_gold, platinum")
    elements: str = Field(..., description="Elements: cars, watches, jewelry, yachts, mansions")
    mood: str = Field(..., description="Mood: luxurious, extravagant, sophisticated, bold, subtle")
    additional_details: Optional[str] = Field(None, description="Any additional details")

class GenerateImageRequest(BaseModel):
    customization: ImageCustomization
    ai_model: str = Field(default="gemini", description="AI model to use: gemini, dalle")

class ImageResponse(BaseModel):
    id: int
    serial: str
    image_url_verified: str
    image_url_wallpaper: str
    created_at: datetime
    payment_status: str
    
    class Config:
        from_attributes = True

class VerifyImageResponse(BaseModel):
    valid: bool
    serial: Optional[str] = None
    created_at: Optional[datetime] = None
    image_url_verified: Optional[str] = None
    user_email: Optional[str] = None

# Payment Schemas (TODO: Implement Stripe integration)
class CreatePaymentIntent(BaseModel):
    image_id: int
    amount: float
    currency: str = "USD"

class PaymentResponse(BaseModel):
    id: int
    amount: float
    status: str
    payment_intent_id: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
