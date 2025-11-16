import qrcode
from io import BytesIO
from PIL import Image

class QRGenerator:
    @staticmethod
    def generate(verification_url: str) -> Image.Image:
        """Generate a QR code image from a verification URL."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(verification_url)
        qr.make(fit=True)
        
        # Create QR code image with white foreground and black background
        qr_img = qr.make_image(fill_color="white", back_color="black")
        return qr_img
