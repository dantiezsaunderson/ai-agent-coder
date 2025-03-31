"""
Test script for Multi-Skill Super-Agent

This script tests the functionality of the multi-skill agent system.
"""
import asyncio
import sys
import os
from loguru import logger

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.code_agent import CodeGenerationAgent
from src.agents.image_agent import ImageGenerationAgent
from src.agents.research_agent import WebResearchAgent
from src.agents.task_agent import TaskAutomationAgent
from src.agents.assistant_agent import PersonalAssistantAgent
from src.orchestration.router import AgentRouter
from src.utils.github_integration import GitHubIntegration
from src.utils.render_deployment import RenderDeployment
from src.utils.config import validate_config

async def test_code_agent():
    """Test the Code Generation Agent"""
    logger.info("Testing Code Generation Agent...")
    
    agent = CodeGenerationAgent()
    result = await agent.process("Create a function to calculate the Fibonacci sequence")
    
    logger.info(f"Code Generation Result:\n{result}")
    return result

async def test_image_agent():
    """Test the Image Generation Agent"""
    logger.info("Testing Image Generation Agent...")
    
    agent = ImageGenerationAgent()
    result = await agent.process("A futuristic city with flying cars")
    
    logger.info(f"Image Generation Result: {result}")
    return result

async def test_research_agent():
    """Test the Web Research Agent"""
    logger.info("Testing Web Research Agent...")
    
    agent = WebResearchAgent()
    result = await agent.process("Latest developments in quantum computing")
    
    logger.info(f"Web Research Result:\n{result}")
    return result

async def test_task_agent():
    """Test the Task Automation Agent"""
    logger.info("Testing Task Automation Agent...")
    
    agent = TaskAutomationAgent()
    result = await agent.process("Schedule a reminder to check emails in 1 minute")
    
    logger.info(f"Task Automation Result: {result}")
    return result

async def test_assistant_agent():
    """Test the Personal Assistant Agent"""
    logger.info("Testing Personal Assistant Agent...")
    
    agent = PersonalAssistantAgent()
    result = await agent.process("Draft an email to schedule a team meeting next week")
    
    logger.info(f"Personal Assistant Result:\n{result}")
    return result

async def test_agent_router():
    """Test the Agent Router"""
    logger.info("Testing Agent Router...")
    
    router = AgentRouter()
    
    code_result = await router.route_to_code_agent("Create a function to sort a list")
    logger.info(f"Router Code Result:\n{code_result}")
    
    image_result = await router.route_to_image_agent("A mountain landscape")
    logger.info(f"Router Image Result: {image_result}")
    
    research_result = await router.route_to_research_agent("Benefits of meditation")
    logger.info(f"Router Research Result:\n{research_result}")
    
    return {
        "code": code_result,
        "image": image_result,
        "research": research_result
    }

async def test_github_integration():
    """Test the GitHub Integration"""
    logger.info("Testing GitHub Integration...")
    
    try:
        github = GitHubIntegration()
        # Create a test file in the repository
        result = await github.create_file(
            path="test/test_file.md",
            content="# Test File\n\nThis is a test file created by the Multi-Skill Super-Agent.",
            message="Test GitHub integration"
        )
        
        logger.info(f"GitHub Integration Result: File created successfully")
        return result
    except Exception as e:
        logger.error(f"GitHub Integration Error: {str(e)}")
        return {"error": str(e)}

async def test_render_deployment():
    """Test the Render Deployment"""
    logger.info("Testing Render Deployment...")
    
    try:
        render = RenderDeployment()
        # Note: This will actually trigger a deployment, so we'll just log what would happen
        logger.info("Render Deployment: Would trigger deployment with hook URL")
        logger.info(f"Render Deploy Hook: {render.deploy_hook}")
        
        # Return a simulated result instead of actually triggering the deployment
        return {
            "status": "simulated",
            "message": "Deployment would be triggered in production environment"
        }
    except Exception as e:
        logger.error(f"Render Deployment Error: {str(e)}")
        return {"error": str(e)}

async def run_tests():
    """Run all tests"""
    logger.info("Starting tests for Multi-Skill Super-Agent...")
    
    # Validate configuration
    if not validate_config():
        logger.error("Configuration validation failed. Exiting tests.")
        return
    
    # Create test results directory
    os.makedirs("tests/results", exist_ok=True)
    
    # Run tests
    test_results = {}
    
    # Test individual agents
    test_results["code_agent"] = await test_code_agent()
    test_results["image_agent"] = await test_image_agent()
    test_results["research_agent"] = await test_research_agent()
    test_results["task_agent"] = await test_task_agent()
    test_results["assistant_agent"] = await test_assistant_agent()
    
    # Test router
    test_results["agent_router"] = await test_agent_router()
    
    # Test integrations
    # Uncomment these in a real test environment
    # test_results["github_integration"] = await test_github_integration()
    # test_results["render_deployment"] = await test_render_deployment()
    
    # Save test results
    with open("tests/results/test_results.txt", "w") as f:
        f.write("# Multi-Skill Super-Agent Test Results\n\n")
        
        for test_name, result in test_results.items():
            f.write(f"## {test_name}\n\n")
            f.write(f"{result}\n\n")
    
    logger.info("Tests completed. Results saved to tests/results/test_results.txt")

if __name__ == "__main__":
    asyncio.run(run_tests())
