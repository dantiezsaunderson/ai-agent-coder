"""
Agent Factory for Multi-Skill Super-Agent

This module provides a factory for creating agent instances.
"""
from loguru import logger

from ..agents.code_agent import CodeGenerationAgent
from ..agents.image_agent import ImageGenerationAgent
from ..agents.research_agent import WebResearchAgent
from ..agents.task_agent import TaskAutomationAgent
from ..agents.assistant_agent import PersonalAssistantAgent

class AgentFactory:
    """Factory for creating agent instances"""
    
    _instances = {}
    
    @classmethod
    def get_code_agent(cls):
        """
        Get or create a CodeGenerationAgent instance
        
        Returns:
            CodeGenerationAgent instance
        """
        if "code" not in cls._instances:
            cls._instances["code"] = CodeGenerationAgent()
            logger.info("Created new CodeGenerationAgent instance")
        return cls._instances["code"]
    
    @classmethod
    def get_image_agent(cls):
        """
        Get or create an ImageGenerationAgent instance
        
        Returns:
            ImageGenerationAgent instance
        """
        if "image" not in cls._instances:
            cls._instances["image"] = ImageGenerationAgent()
            logger.info("Created new ImageGenerationAgent instance")
        return cls._instances["image"]
    
    @classmethod
    def get_research_agent(cls):
        """
        Get or create a WebResearchAgent instance
        
        Returns:
            WebResearchAgent instance
        """
        if "research" not in cls._instances:
            cls._instances["research"] = WebResearchAgent()
            logger.info("Created new WebResearchAgent instance")
        return cls._instances["research"]
    
    @classmethod
    def get_task_agent(cls):
        """
        Get or create a TaskAutomationAgent instance
        
        Returns:
            TaskAutomationAgent instance
        """
        if "task" not in cls._instances:
            cls._instances["task"] = TaskAutomationAgent()
            logger.info("Created new TaskAutomationAgent instance")
        return cls._instances["task"]
    
    @classmethod
    def get_assistant_agent(cls):
        """
        Get or create a PersonalAssistantAgent instance
        
        Returns:
            PersonalAssistantAgent instance
        """
        if "assistant" not in cls._instances:
            cls._instances["assistant"] = PersonalAssistantAgent()
            logger.info("Created new PersonalAssistantAgent instance")
        return cls._instances["assistant"]
