"""
AI Models Configuration

This file contains the configuration for all supported AI image generation models.
To add a new model, simply add its configuration here.
"""

AI_MODELS = {
    "gemini": {
        "name": "Google Gemini",
        "provider": "Google",
        "model_id": "imagen-3.0-generate-002",
        "env_key": "GEMINI_API_KEY",
        "description": "High-quality image generation with Imagen 3.0",
        "supported_sizes": ["1024x1024", "1024x1792", "1792x1024"],
        "default_size": "1024x1792",
        "cost_per_image": 0.04,  # Approximate
    },
    "dalle": {
        "name": "DALL-E 3",
        "provider": "OpenAI",
        "model_id": "dall-e-3",
        "env_key": "OPENAI_API_KEY",
        "description": "Ultra HD image generation with DALL-E 3",
        "supported_sizes": ["1024x1024", "1024x1792", "1792x1024"],
        "default_size": "1024x1792",
        "cost_per_image": 0.080,  # HD quality
    },
    "dalle2": {
        "name": "DALL-E 2",
        "provider": "OpenAI",
        "model_id": "dall-e-2",
        "env_key": "OPENAI_API_KEY",
        "description": "Fast and affordable image generation",
        "supported_sizes": ["1024x1024"],
        "default_size": "1024x1024",
        "cost_per_image": 0.020,
    },
    # Add more models here as needed:
    # "midjourney": {...},
    # "stable-diffusion": {...},
    # "firefly": {...},
}

def get_model_config(model_name: str):
    """Get configuration for a specific model."""
    if model_name not in AI_MODELS:
        raise ValueError(f"Unknown model: {model_name}. Available models: {list(AI_MODELS.keys())}")
    return AI_MODELS[model_name]

def list_available_models():
    """List all available models."""
    return [
        {
            "id": model_id,
            "name": config["name"],
            "provider": config["provider"],
            "description": config["description"],
        }
        for model_id, config in AI_MODELS.items()
    ]
