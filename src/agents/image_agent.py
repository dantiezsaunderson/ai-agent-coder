"""
Image Generation Agent for Multi-Skill Super-Agent

This module implements the Image Generation Agent that generates images
based on user requests using the OpenAI DALL-E API.
"""
import openai
from loguru import logger

from .base_agent import Agent
from ..utils.config import OPENAI_API_KEY

class ImageGenerationAgent(Agent):
    """Agent for generating images using OpenAI DALL-E API"""
    
    def __init__(self):
        """Initialize the image generation agent"""
        super().__init__("ImageGeneration")
        openai.api_key = OPENAI_API_KEY
    
    async def process(self, query: str) -> str:
        """
        Process an image generation query and return image URL
        
        Args:
            query: The image generation query
            
        Returns:
            The URL of the generated image
        """
        try:
            # Pre-process the query
            processed_query = await self._pre_process(query)
            
            # Call OpenAI API to generate image
            response = await openai.images.generate(
                model="dall-e-3",
                prompt=processed_query,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            # Extract the image URL
            image_url = response.data[0].url
            
            # Post-process the response
            return await self._post_process(image_url)
        
        except Exception as e:
            logger.error(f"Error in image generation: {str(e)}")
            return f"Error generating image: {str(e)}"
    
    async def _pre_process(self, query: str) -> str:
        """
        Pre-process an image generation query
        
        Args:
            query: The query to pre-process
            
        Returns:
            The pre-processed query
        """
        # Enhance the prompt for better image generation
        enhanced_query = (
            f"Create a detailed, high-quality image of: {query}. "
            f"The image should be well-composed with good lighting and detail."
        )
        return enhanced_query
