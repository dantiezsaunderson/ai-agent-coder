"""
Task Automation Agent for Multi-Skill Super-Agent

This module implements the Task Automation Agent that handles recurring tasks,
reminders, and system triggers.
"""
from datetime import datetime, timedelta
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from .base_agent import Agent
from ..persistence.database import DatabaseManager

class TaskAutomationAgent(Agent):
    """Agent for task automation and scheduling"""
    
    def __init__(self):
        """Initialize the task automation agent"""
        super().__init__("TaskAutomation")
        self.scheduler = AsyncIOScheduler()
        self.db_manager = DatabaseManager()
        self.scheduler.start()
        logger.info("Task automation agent initialized with scheduler")
    
    async def process(self, query: str) -> str:
        """
        Process a task automation query and schedule or manage tasks
        
        Args:
            query: The task automation query
            
        Returns:
            The result of the task automation request
        """
        try:
            # Pre-process the query
            processed_query = await self._pre_process(query)
            
            # Parse the query to determine the task type
            if "schedule" in processed_query.lower() or "remind" in processed_query.lower():
                result = await self._schedule_task(processed_query)
            elif "list" in processed_query.lower() or "show" in processed_query.lower():
                result = await self._list_tasks()
            elif "cancel" in processed_query.lower() or "delete" in processed_query.lower():
                result = await self._cancel_task(processed_query)
            else:
                result = "I'm not sure what task automation action to perform. Try asking to schedule, list, or cancel tasks."
            
            # Post-process the response
            return await self._post_process(result)
        
        except Exception as e:
            logger.error(f"Error in task automation: {str(e)}")
            return f"Error in task automation: {str(e)}"
    
    async def _schedule_task(self, query: str) -> str:
        """
        Schedule a new task based on the query
        
        Args:
            query: The task scheduling query
            
        Returns:
            Confirmation message
        """
        # This is a simplified implementation
        # In a real implementation, this would parse the query for task details and schedule it
        logger.info(f"Scheduling task: {query}")
        
        # Save task to database
        task_record = self.db_manager.add_task_record(
            task_type="scheduled_task",
            query=query,
            status="pending"
        )
        
        # For demonstration, we'll just schedule a task to run after 1 minute
        # In a real implementation, this would parse the time from the query
        task_id = task_record['id']
        run_date = datetime.utcnow() + timedelta(minutes=1)
        
        self.scheduler.add_job(
            self._execute_task,
            'date',
            run_date=run_date,
            args=[task_id, query],
            id=f"task_{task_id}"
        )
        
        return f"Task scheduled with ID {task_id} to run at {run_date.strftime('%Y-%m-%d %H:%M:%S UTC')}"
    
    async def _list_tasks(self) -> str:
        """
        List all scheduled tasks
        
        Returns:
            List of scheduled tasks
        """
        # Get scheduled jobs from the scheduler
        jobs = self.scheduler.get_jobs()
        
        if not jobs:
            return "No tasks are currently scheduled."
        
        task_list = "Scheduled tasks:\n\n"
        for job in jobs:
            task_list += f"- Task ID: {job.id}\n"
            task_list += f"  Run time: {job.next_run_time.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            task_list += f"  Args: {job.args}\n\n"
        
        return task_list
    
    async def _cancel_task(self, query: str) -> str:
        """
        Cancel a scheduled task
        
        Args:
            query: The task cancellation query
            
        Returns:
            Confirmation message
        """
        # This is a simplified implementation
        # In a real implementation, this would parse the task ID from the query
        logger.info(f"Cancelling task: {query}")
        
        # Extract task ID from query (simplified)
        # In a real implementation, this would use NLP to extract the task ID
        parts = query.split()
        task_id = None
        for i, part in enumerate(parts):
            if part.lower() == "id" and i < len(parts) - 1:
                try:
                    task_id = int(parts[i + 1])
                    break
                except ValueError:
                    pass
        
        if task_id is None:
            return "Could not determine which task to cancel. Please provide a task ID."
        
        # Try to remove the job from the scheduler
        job_id = f"task_{task_id}"
        try:
            self.scheduler.remove_job(job_id)
            
            # Update task status in database
            self.db_manager.update_task_record(
                task_id=task_id,
                status="cancelled"
            )
            
            return f"Task with ID {task_id} has been cancelled."
        except Exception as e:
            logger.error(f"Error cancelling task {task_id}: {str(e)}")
            return f"Could not cancel task with ID {task_id}. It may not exist or has already completed."
    
    async def _execute_task(self, task_id: int, task_description: str):
        """
        Execute a scheduled task
        
        Args:
            task_id: The ID of the task to execute
            task_description: The description of the task
        """
        logger.info(f"Executing task {task_id}: {task_description}")
        
        try:
            # This is where the actual task execution would happen
            # For demonstration, we'll just update the task status
            
            # Update task status in database
            self.db_manager.update_task_record(
                task_id=task_id,
                result="Task executed successfully",
                status="success"
            )
            
            logger.info(f"Task {task_id} executed successfully")
        except Exception as e:
            logger.error(f"Error executing task {task_id}: {str(e)}")
            
            # Update task status in database
            self.db_manager.update_task_record(
                task_id=task_id,
                result=f"Error executing task: {str(e)}",
                status="error"
            )
