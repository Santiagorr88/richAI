import os
import asyncio
from typing import Dict, Any, Optional
import openai
import requests
from io import BytesIO
import google.generativeai as genai

class ImageGeneratorService:
    def __init__(self):
        # Google Gemini setup
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key and self.gemini_api_key != "your-gemini-api-key-here":
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_configured = True
            except Exception as e:
                print(f"Warning: Gemini setup failed: {e}")
                self.gemini_configured = False
        else:
            self.gemini_configured = False
        
        # OpenAI setup
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key and self.openai_api_key != "your-openai-api-key-here":
            openai.api_key = self.openai_api_key
            self.openai_configured = True
        else:
            self.openai_configured = False
    
    def build_prompt(self, customization: Dict[str, Any]) -> str:
        """Build a detailed prompt based on user customization."""
        style = customization.get("style", "elegant")
        color_scheme = customization.get("color_scheme", "gold")
        elements = customization.get("elements", "luxury")
        mood = customization.get("mood", "luxurious")
        additional = customization.get("additional_details", "")
        
        # Map color schemes to descriptions
        color_map = {
            "gold": "golden and warm tones",
            "silver": "silver and cool metallic tones",
            "black_gold": "black with gold accents",
            "rose_gold": "rose gold and pink metallic tones",
            "platinum": "platinum and white metallic tones"
        }
        
        # Map elements to descriptions
        elements_map = {
            "cars": "luxury sports cars and supercars",
            "watches": "expensive watches and timepieces",
            "jewelry": "diamonds, gold jewelry, and precious gems",
            "yachts": "luxury yachts and private boats",
            "mansions": "penthouses and luxury real estate"
        }
        
        color_desc = color_map.get(color_scheme, "gold and luxurious tones")
        elements_desc = elements_map.get(elements, "symbols of wealth and luxury")
        
        prompt = f"""Create a hyper-realistic, vertical 9:16 high-resolution image that screams extreme wealth and luxury.

Style: {style} and {mood}
Color Scheme: Emphasize {color_desc}
Main Elements: Feature {elements_desc}

The image MUST include the text "I'm Rich" prominently displayed as a bold, elegant logo or title.

The overall composition should be:
- Aspirational and premium
- Visually striking and flashy
- Perfect for a mobile wallpaper (vertical format)
- No nudity or explicit content
- Just over-the-top luxury and opulence

{additional if additional else ''}

Make it look like modern wealth in 2025 - think exclusive nightlife, private jets, designer brands, and ultimate luxury lifestyle."""
        
        return prompt
    
    async def generate_image(
        self,
        customization: Dict[str, Any],
        model: str = "gemini"
    ) -> bytes:
        """Generate an image using the specified AI model."""
        prompt = self.build_prompt(customization)
        
        if model == "gemini":
            if not self.gemini_generator:
                raise ValueError("Gemini API key not configured. Please add GEMINI_API_KEY to .env file")
            
            images = await self.gemini_generator.generate_images(
                prompt=prompt,
                model="imagen-3.0-generate-002",
                number_of_images=1
            )
            return images[0]
        
        elif model == "dalle":
            if not self.openai_api_key:
                raise ValueError("OpenAI API key not configured. Please add OPENAI_API_KEY to .env file")
            
            # Generate image with DALL-E 3
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792",  # Vertical format
                quality="hd",
                n=1,
            )
            
            # Download the image
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            return image_response.content
        
        elif model == "dalle2":
            if not self.openai_api_key:
                raise ValueError("OpenAI API key not configured. Please add OPENAI_API_KEY to .env file")
            
            # DALL-E 2 (cheaper, faster but lower quality)
            response = openai.images.generate(
                model="dall-e-2",
                prompt=prompt,
                size="1024x1024",  # DALL-E 2 only supports square
                n=1,
            )
            
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            return image_response.content
        
        else:
            raise ValueError(f"Unsupported AI model: {model}. Available models: gemini, dalle, dalle2")
    
    def get_prompt_for_record(self, customization: Dict[str, Any]) -> str:
        """Get the prompt that will be stored in database."""
        return self.build_prompt(customization)
