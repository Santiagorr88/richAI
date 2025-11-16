from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

class ImageComposer:
    @staticmethod
    def create_verified_image(
        base_image_bytes: bytes,
        qr_image: Image.Image,
        serial: str
    ) -> bytes:
        """Create an image with QR code and serial number (for verification)."""
        # Open the base image
        base_image = Image.open(BytesIO(base_image_bytes)).convert("RGBA")
        
        # Resize QR code to appropriate size (150x150)
        qr_size = 150
        qr_resized = qr_image.resize((qr_size, qr_size)).convert("RGBA")
        
        # Position QR in bottom-left corner with margin
        margin = 20
        qr_position = (margin, base_image.height - qr_size - margin)
        
        # Paste QR code on base image
        base_image.paste(qr_resized, qr_position, qr_resized)
        
        # Add serial number text below QR code
        draw = ImageDraw.Draw(base_image)
        
        # Try to use a better font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        serial_text = f"Serial: {serial}"
        
        # Get text size using textbbox
        bbox = draw.textbbox((0, 0), serial_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position text below QR code
        text_position = (margin, base_image.height - margin + 5)
        
        # Draw text with shadow for better visibility
        shadow_offset = 2
        draw.text(
            (text_position[0] + shadow_offset, text_position[1] + shadow_offset),
            serial_text,
            font=font,
            fill="black"
        )
        draw.text(
            text_position,
            serial_text,
            font=font,
            fill="white"
        )
        
        # Convert back to RGB for saving as JPEG (smaller file size)
        final_image = base_image.convert("RGB")
        
        # Save to bytes
        output = BytesIO()
        final_image.save(output, format="JPEG", quality=95)
        output.seek(0)
        
        return output.getvalue()
    
    @staticmethod
    def create_wallpaper_image(base_image_bytes: bytes) -> bytes:
        """Create a clean wallpaper image without QR/serial (for actual use)."""
        # Open the base image
        base_image = Image.open(BytesIO(base_image_bytes))
        
        # Convert to RGB if needed
        if base_image.mode == "RGBA":
            base_image = base_image.convert("RGB")
        
        # Save to bytes
        output = BytesIO()
        base_image.save(output, format="JPEG", quality=95)
        output.seek(0)
        
        return output.getvalue()
