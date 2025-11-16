from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import json
from dotenv import load_dotenv

from database import get_db, init_db
from models import User, Image, Payment
from schemas import (
    UserRegister, UserLogin, Token, UserResponse,
    GenerateImageRequest, ImageResponse, VerifyImageResponse,
    CreatePaymentIntent, PaymentResponse
)
from auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, get_optional_user
)
from services.image_generator import ImageGeneratorService
from services.serial_generator import SerialGenerator
from services.qr_generator import QRGenerator
from services.image_composer import ImageComposer

load_dotenv()

app = FastAPI(title="I'm Rich AI API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://geminirich.preview.emergentagent.com",
        "https://*.preview.emergentagent.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create generated images directory
os.makedirs("/app/generated", exist_ok=True)

# Mount static files for serving generated images
app.mount("/images", StaticFiles(directory="/app/generated"), name="images")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "I'm Rich AI API"}

@app.get("/api/models")
async def list_models():
    """List all available AI models."""
    from services.ai_models_config import list_available_models
    return {"models": list_available_models()}

# ==================== Authentication Endpoints ====================

@app.post("/api/auth/register", response_model=Token)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# TODO: Implement OAuth endpoints (Google, Apple)
# @app.get("/api/auth/google")
# async def google_oauth():
#     # Implement Google OAuth flow
#     # 1. Redirect to Google OAuth consent screen
#     # 2. Handle callback with authorization code
#     # 3. Exchange code for access token
#     # 4. Get user info from Google
#     # 5. Create or login user
#     # 6. Return JWT token
#     pass

# @app.get("/api/auth/apple")
# async def apple_oauth():
#     # Implement Apple OAuth flow
#     # Similar to Google but with Apple's Sign in with Apple
#     pass

# ==================== Image Generation Endpoints ====================

@app.post("/api/generate-image", response_model=ImageResponse)
async def generate_image(
    request: GenerateImageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Initialize image generator service
        generator = ImageGeneratorService()
        
        # Generate unique serial
        serial = SerialGenerator.generate()
        
        # Generate AI image
        customization_dict = request.customization.dict()
        base_image_bytes = await generator.generate_image(
            customization=customization_dict,
            model=request.ai_model
        )
        
        # Generate QR code
        base_url = os.getenv("BASE_URL", "http://localhost:3000")
        verification_url = f"{base_url}/verify/{serial}"
        qr_image = QRGenerator.generate(verification_url)
        
        # Create two versions of the image
        # 1. Verified version (with QR + serial)
        verified_image_bytes = ImageComposer.create_verified_image(
            base_image_bytes, qr_image, serial
        )
        
        # 2. Wallpaper version (clean, no QR/serial)
        wallpaper_image_bytes = ImageComposer.create_wallpaper_image(base_image_bytes)
        
        # Save images
        verified_path = f"/app/generated/{serial}_verified.jpg"
        wallpaper_path = f"/app/generated/{serial}_wallpaper.jpg"
        
        with open(verified_path, "wb") as f:
            f.write(verified_image_bytes)
        
        with open(wallpaper_path, "wb") as f:
            f.write(wallpaper_image_bytes)
        
        # Store in database
        prompt_used = generator.get_prompt_for_record(customization_dict)
        new_image = Image(
            user_id=current_user.id,
            serial=serial,
            image_path_verified=verified_path,
            image_path_wallpaper=wallpaper_path,
            prompt=prompt_used,
            customization=json.dumps(customization_dict),
            payment_status="pending"  # Will be updated after payment
        )
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
        
        # TODO: Send email with images
        # await send_email_with_images(
        #     to=current_user.email,
        #     serial=serial,
        #     verified_image_path=verified_path,
        #     wallpaper_image_path=wallpaper_path
        # )
        
        return ImageResponse(
            id=new_image.id,
            serial=new_image.serial,
            image_url_verified=f"/api/images/{serial}_verified.jpg",
            image_url_wallpaper=f"/api/images/{serial}_wallpaper.jpg",
            created_at=new_image.created_at,
            payment_status=new_image.payment_status
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating image: {str(e)}"
        )

@app.get("/api/images/{filename}")
async def get_image(filename: str):
    """Serve generated images."""
    file_path = f"/app/generated/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@app.get("/api/verify/{serial}", response_model=VerifyImageResponse)
async def verify_image(serial: str, db: Session = Depends(get_db)):
    """Verify if an image serial is authentic."""
    image = db.query(Image).filter(Image.serial == serial).first()
    
    if not image:
        return VerifyImageResponse(valid=False)
    
    user = db.query(User).filter(User.id == image.user_id).first()
    
    return VerifyImageResponse(
        valid=True,
        serial=image.serial,
        created_at=image.created_at,
        image_url_verified=f"/api/images/{serial}_verified.jpg",
        user_email=user.email if user else None
    )

@app.get("/api/my-images", response_model=List[ImageResponse])
async def get_my_images(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all images for the current user."""
    images = db.query(Image).filter(Image.user_id == current_user.id).order_by(Image.created_at.desc()).all()
    
    return [
        ImageResponse(
            id=img.id,
            serial=img.serial,
            image_url_verified=f"/api/images/{img.serial}_verified.jpg",
            image_url_wallpaper=f"/api/images/{img.serial}_wallpaper.jpg",
            created_at=img.created_at,
            payment_status=img.payment_status
        )
        for img in images
    ]

# ==================== Payment Endpoints (TODO: Stripe Integration) ====================

@app.post("/api/payments/create-intent", response_model=dict)
async def create_payment_intent(
    payment_data: CreatePaymentIntent,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe payment intent."""
    # TODO: Implement Stripe payment intent creation
    # 
    # Steps:
    # 1. Import stripe library: import stripe
    # 2. Set API key: stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    # 3. Create payment intent:
    #    intent = stripe.PaymentIntent.create(
    #        amount=int(payment_data.amount * 100),  # Convert to cents
    #        currency=payment_data.currency.lower(),
    #        metadata={"image_id": payment_data.image_id, "user_id": current_user.id}
    #    )
    # 4. Create Payment record in database
    # 5. Return client_secret to frontend
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Stripe integration not yet configured. Please add STRIPE_SECRET_KEY to .env"
    )

@app.post("/api/payments/webhook")
async def stripe_webhook(db: Session = Depends(get_db)):
    """Handle Stripe webhook events."""
    # TODO: Implement Stripe webhook handler
    # 
    # Steps:
    # 1. Verify webhook signature using STRIPE_WEBHOOK_SECRET
    # 2. Handle different event types:
    #    - payment_intent.succeeded: Mark payment as completed, send email
    #    - payment_intent.payment_failed: Mark payment as failed
    # 3. Update Payment and Image records in database
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Stripe webhook not yet configured"
    )

@app.get("/api/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get payment details."""
    payment = db.query(Payment).filter(
        Payment.id == payment_id,
        Payment.user_id == current_user.id
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return payment

# ==================== Email Service (TODO: SendGrid Integration) ====================

# async def send_email_with_images(
#     to: str,
#     serial: str,
#     verified_image_path: str,
#     wallpaper_image_path: str
# ):
#     """Send email with generated images."""
#     # TODO: Implement SendGrid email sending
#     # 
#     # Steps:
#     # 1. Import sendgrid library
#     # 2. Create SendGrid client with API key
#     # 3. Build email with:
#     #    - Subject: "Your I'm Rich AI Image - Serial #{serial}"
#     #    - HTML body with instructions
#     #    - Attach both images
#     # 4. Send email
#     # 5. Log result
#     
#     pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
