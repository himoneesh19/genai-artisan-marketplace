import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.preview.vision_models import ImageGenerationModel
import os
import json
import tempfile
import uuid
from config import Config
from google.auth.credentials import Credentials
from google.oauth2 import service_account

def initialize_vertex_ai():
    """Initialize Vertex AI with credentials from .env or fallback to file"""
    credentials = Config.get_service_account_credentials()

    if credentials:
        # Use service account credentials from .env
        print("Using service account credentials from .env")
        creds = service_account.Credentials.from_service_account_info(credentials)
        vertexai.init(project=Config.GOOGLE_CLOUD_PROJECT, location=Config.VERTEX_AI_LOCATION, credentials=creds)
    elif Config.VERTEX_AI_API_KEY:
        # Use API key for text generation - but image generation will fail
        print("Using API key for VertexAI (text only)")
        class APIKeyCredentials(Credentials):
            def __init__(self, api_key):
                super().__init__()
                self.api_key = api_key
            def apply(self, headers, token=None):
                headers['x-goog-api-key'] = self.api_key
            def refresh(self, request):
                pass
        creds = APIKeyCredentials(Config.VERTEX_AI_API_KEY)
        vertexai.init(project=Config.GOOGLE_CLOUD_PROJECT, location=Config.VERTEX_AI_LOCATION, credentials=creds)
    else:
        # Fallback to default credentials (JSON file or environment)
        print("Using default credentials (JSON file)")
        vertexai.init(project=Config.GOOGLE_CLOUD_PROJECT, location=Config.VERTEX_AI_LOCATION)

def get_text_credentials():
    """Get credentials for text generation (supports API key)"""
    credentials = Config.get_service_account_credentials()

    if credentials:
        # Use service account credentials
        return service_account.Credentials.from_service_account_info(credentials)
    elif Config.VERTEX_AI_API_KEY:
        # Use API key for text generation
        class APIKeyCredentials(Credentials):
            def __init__(self, api_key):
                super().__init__()
                self.api_key = api_key
            def apply(self, headers, token=None):
                headers['x-goog-api-key'] = self.api_key
            def refresh(self, request):
                pass
        return APIKeyCredentials(Config.VERTEX_AI_API_KEY)
    else:
        # Fallback to default credentials
        return None

def generate_text(prompt, max_tokens=500):
    """
    Generate text using Vertex AI Gemini model with fallback for model availability
    """
    model_names = ["gemini-1.5-flash", "gemini-1.5-pro"]
    last_error = None
    for model_name in model_names:
        try:
            model = GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config={"max_output_tokens": max_tokens}
            )
            return response.text
        except Exception as e:
            last_error = e
            # If 404 error, try next model
            if "404" in str(e) or "not available" in str(e).lower():
                continue
            else:
                return f"Error generating text: {str(e)}"
    return f"Error generating text: {str(last_error)}"

def generate_image(prompt, aspect_ratio="1:1"):
    """
    Generate image using Vertex AI Image Generation Model (Imagen)
    Note: Imagen requires OAuth2 credentials, not API keys
    """
    try:
        # Check if we have service account credentials for image generation
        credentials = Config.get_service_account_credentials()
        if credentials and Config.VERTEX_AI_API_KEY:
            # Temporarily reinitialize with service account for image generation
            creds = service_account.Credentials.from_service_account_info(credentials)
            vertexai.init(project=Config.GOOGLE_CLOUD_PROJECT, location=Config.VERTEX_AI_LOCATION, credentials=creds)

        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio=aspect_ratio
        )
        image = response.images[0]
        # Generate unique filename
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join("static", "images", filename)
        image.save(filepath)

        # Reinitialize with API key for text generation if needed
        if Config.VERTEX_AI_API_KEY and credentials:
            class APIKeyCredentials(Credentials):
                def __init__(self, api_key):
                    super().__init__()
                    self.api_key = api_key
                def apply(self, headers, token=None):
                    headers['x-goog-api-key'] = self.api_key
                def refresh(self, request):
                    pass
            creds = APIKeyCredentials(Config.VERTEX_AI_API_KEY)
            vertexai.init(project=Config.GOOGLE_CLOUD_PROJECT, location=Config.VERTEX_AI_LOCATION, credentials=creds)

        return filename
    except Exception as e:
        raise Exception(f"Error generating image: {str(e)}")

def generate_marketing_copy(prompt):
    """
    Generate marketing copy for artisan's craft
    """
    return generate_text(prompt)

def generate_social_media_post(craft_description, platform="Instagram"):
    """
    Generate social media post content
    """
    prompt = f"Create a {platform} post about this craft: {craft_description}. Include emojis and hashtags suitable for the platform."
    return generate_text(prompt)

def generate_craft_story(craft_description):
    """
    Generate a story about the artisan and their craft
    """
    prompt = f"Write an inspiring story about an artisan and their craft. Description: {craft_description}. Focus on tradition, passion, and cultural heritage."
    return generate_text(prompt)

def generate_product_visual_description(product_name, craft_type):
    """
    Generate a detailed description for image generation
    """
    prompt = f"Describe a high-quality, professional photograph of a {craft_type} product called '{product_name}'. Include details about lighting, composition, and style to make it appealing for marketing."
    return generate_text(prompt)
