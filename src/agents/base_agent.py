"""
Base Agent class for Multi-Skill Super-Agent

This module defines the base Agent class that all specific agent implementations will inherit from.
"""
from abc import ABC, abstractmethod
from loguru import logger

class Agent(ABC):
    """Base class for all agent implementations"""
    
    def __init__(self, name: str):
        """
        Initialize the agent
        
        Args:
            name: The name of the agent
        """
        self.name = name
        logger.info(f"{name} agent initialized")
    
    @abstractmethod
    async def process(self, query: str) -> str:
        """
        Process a query and return a response
        
        Args:
            query: The query to process
            
        Returns:
            The response to the query
        """
        pass
    
    async def _pre_process(self, query: str) -> str:
        """
        Pre-process a query before processing
        
        Args:
            query: The query to pre-process
            
        Returns:
            The pre-processed query
        """
        return query
    
    async def _post_process(self, response: str) -> str:
        """
        Post-process a response after processing
        
        Args:
            response: The response to post-process
            
        Returns:
            The post-processed response
        """
        return response
