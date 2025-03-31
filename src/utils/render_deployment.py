"""
Render Deployment Integration for Multi-Skill Super-Agent

This module handles deployment to Render using deployment hooks.
"""
import requests
from loguru import logger

from ..utils.config import RENDER_DEPLOY_HOOK

class RenderDeployment:
    """Render deployment integration for deploying applications"""
    
    def __init__(self):
        """Initialize the Render deployment integration"""
        self.deploy_hook = RENDER_DEPLOY_HOOK
        logger.info("Render deployment integration initialized")
    
    async def trigger_deployment(self) -> dict:
        """
        Trigger a deployment on Render
        
        Returns:
            Response from Render API
        """
        try:
            if not self.deploy_hook:
                raise ValueError("Render deploy hook URL is not configured")
            
            logger.info("Triggering deployment on Render")
            
            # Send POST request to the deploy hook URL
            response = requests.post(self.deploy_hook)
            response.raise_for_status()
            
            logger.info("Deployment triggered successfully")
            return {
                "status": "success",
                "message": "Deployment triggered successfully",
                "response_code": response.status_code
            }
        
        except Exception as e:
            logger.error(f"Error triggering deployment: {str(e)}")
            return {
                "status": "error",
                "message": f"Error triggering deployment: {str(e)}"
            }
    
    async def deploy_project(self, github_repo: str = None) -> dict:
        """
        Deploy a project to Render
        
        Args:
            github_repo: GitHub repository to deploy (optional)
            
        Returns:
            Deployment status
        """
        try:
            # Log the deployment request
            if github_repo:
                logger.info(f"Deploying project from GitHub repository: {github_repo}")
            else:
                logger.info("Deploying project using configured deploy hook")
            
            # Trigger the deployment
            result = await self.trigger_deployment()
            
            if result["status"] == "success":
                return {
                    "status": "success",
                    "message": "Deployment initiated successfully. It may take a few minutes to complete.",
                    "details": result
                }
            else:
                return result
        
        except Exception as e:
            logger.error(f"Error deploying project: {str(e)}")
            return {
                "status": "error",
                "message": f"Error deploying project: {str(e)}"
            }
