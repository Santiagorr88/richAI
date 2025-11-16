import os
import asyncio
from typing import Dict, Any, Optional
from emergentintegrations.llm.gemeni.image_generation import GeminiImageGeneration
import openai
import requests
from io import BytesIO

class ImageGeneratorService:
    def __init__(self):
        # Google Gemini setup
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_generator = None
        if self.gemini_api_key and self.gemini_api_key != "your-gemini-api-key-here":
            try:
                self.gemini_generator = GeminiImageGeneration(api_key=self.gemini_api_key)
            except Exception as e:
                print(f"Warning: Gemini setup failed: {e}")
        
        # OpenAI setup
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key and self.openai_api_key != "your-openai-api-key-here":
            openai.api_key = self.openai_api_key
    
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
            images = await self.gemini_generator.generate_images(
                prompt=prompt,
                model="imagen-3.0-generate-002",
                number_of_images=1
            )
            return images[0]
        elif model == "dalle":
            # TODO: Implement DALL-E integration when needed
            # Will need OpenAI API key configuration
            raise NotImplementedError("DALL-E integration not yet implemented. Configure OpenAI API key to use.")
        else:
            raise ValueError(f"Unsupported AI model: {model}")
    
    def get_prompt_for_record(self, customization: Dict[str, Any]) -> str:
        """Get the prompt that will be stored in database."""
        return self.build_prompt(customization)
