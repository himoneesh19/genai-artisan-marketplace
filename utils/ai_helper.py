import vertexai
from vertexai.generative_models import GenerativeModel
# from vertexai.vision_models import ImageGenerationModel  # Commented out due to import issues
import os
from config import Config

def initialize_vertex_ai():
    vertexai.init(project=Config.GOOGLE_CLOUD_PROJECT, location=Config.VERTEX_AI_LOCATION)

def generate_text(prompt, max_tokens=500):
    """
    Generate text using Vertex AI Generative Model (e.g., PaLM)
    """
    try:
        model = GenerativeModel("gemini-1.5-flash")  # Using Gemini model
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating text: {str(e)}"

def generate_image(prompt, aspect_ratio="1:1"):
    """
    Generate image using Vertex AI Image Generation Model (Imagen)
    Note: Image generation is currently disabled due to API changes.
    """
    return "Image generation is currently not available. Please check back later."

def generate_marketing_copy(craft_description, target_audience="general"):
    """
    Generate marketing copy for artisan's craft
    """
    prompt = f"Write compelling marketing copy for a traditional craft product. Description: {craft_description}. Target audience: {target_audience}. Make it engaging and highlight the unique, handmade nature."
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
