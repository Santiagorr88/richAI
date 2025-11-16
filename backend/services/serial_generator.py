import uuid
from datetime import datetime

class SerialGenerator:
    @staticmethod
    def generate() -> str:
        """Generate a unique serial number for an image."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"RICH-{timestamp}-{unique_id}"
