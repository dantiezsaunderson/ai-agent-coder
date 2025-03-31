"""
Code Generation Agent for Multi-Skill Super-Agent

This module implements the Code Generation Agent that generates Python code
based on user requests using the OpenAI API.
"""
import openai
from loguru import logger

from .base_agent import Agent
from ..utils.config import OPENAI_API_KEY

class CodeGenerationAgent(Agent):
    """Agent for generating code using OpenAI API"""
    
    def __init__(self):
        """Initialize the code generation agent"""
        super().__init__("CodeGeneration")
        openai.api_key = OPENAI_API_KEY
    
    async def process(self, query: str) -> str:
        """
        Process a code generation query and return generated code
        
        Args:
            query: The code generation query
            
        Returns:
            The generated code
        """
        try:
            # Pre-process the query
            processed_query = await self._pre_process(query)
            
            # Create a system message for code generation
            system_message = (
                "You are an expert Python programmer. "
                "Generate clean, efficient, and well-documented Python code "
                "based on the user's request. Include comments explaining key parts "
                "of the code. Only respond with code, no explanations outside of code comments."
            )
            
            # Call OpenAI API to generate code
            response = await openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": processed_query}
                ],
                temperature=0.2,  # Lower temperature for more deterministic code generation
                max_tokens=2000
            )
            
            # Extract the generated code
            generated_code = response.choices[0].message.content
            
            # Post-process the response
            return await self._post_process(generated_code)
        
        except Exception as e:
            logger.error(f"Error in code generation: {str(e)}")
            return f"# Error generating code: {str(e)}"
    
    async def _pre_process(self, query: str) -> str:
        """
        Pre-process a code generation query
        
        Args:
            query: The query to pre-process
            
        Returns:
            The pre-processed query
        """
        # Add specific instructions to improve code generation
        enhanced_query = (
            f"Generate Python code for the following request: {query}\n\n"
            f"Requirements:\n"
            f"- Include proper error handling\n"
            f"- Use type hints\n"
            f"- Follow PEP 8 style guidelines\n"
            f"- Include docstrings for functions and classes\n"
            f"- Make the code modular and reusable"
        )
        return enhanced_query
