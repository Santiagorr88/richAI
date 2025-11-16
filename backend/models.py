from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    images = relationship("Image", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    serial = Column(String, unique=True, index=True, nullable=False)
    image_path_verified = Column(String, nullable=False)  # Image with QR/Serial
    image_path_wallpaper = Column(String, nullable=False)  # Clean image for wallpaper
    prompt = Column(Text, nullable=False)
    customization = Column(Text, nullable=True)  # JSON string with user choices
    created_at = Column(DateTime, default=datetime.utcnow)
    payment_status = Column(String, default="pending")  # pending, completed, failed
    
    user = relationship("User", back_populates="images")
    payment = relationship("Payment", back_populates="image", uselist=False)

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="pending")  # pending, completed, failed, refunded
    payment_intent_id = Column(String, nullable=True)  # Stripe payment intent ID
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="payments")
    image = relationship("Image", back_populates="payment")
