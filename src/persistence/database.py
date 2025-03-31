"""
Database module for Multi-Skill Super-Agent

This module handles database operations for storing task history and agent state.
"""
import os
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger

from ..utils.config import DATABASE_URL

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class TaskRecord(Base):
    """Task history record model"""
    __tablename__ = 'task_history'
    
    id = Column(Integer, primary_key=True)
    task_type = Column(String(50), nullable=False)  # code, image, research, etc.
    query = Column(Text, nullable=False)
    result = Column(Text, nullable=True)
    status = Column(String(20), nullable=False)  # success, error, pending
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def to_dict(self):
        """Convert record to dictionary"""
        return {
            'id': self.id,
            'task_type': self.task_type,
            'query': self.query,
            'result': self.result,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class AgentState(Base):
    """Agent state model"""
    __tablename__ = 'agent_state'
    
    id = Column(Integer, primary_key=True)
    agent_name = Column(String(50), nullable=False, unique=True)
    state_data = Column(Text, nullable=False)  # JSON serialized state
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert record to dictionary"""
        return {
            'id': self.id,
            'agent_name': self.agent_name,
            'state_data': json.loads(self.state_data),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DatabaseManager:
    """Manager for database operations"""
    
    def __init__(self):
        """Initialize the database manager"""
        self._create_tables()
        logger.info("Database manager initialized")
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        Base.metadata.create_all(engine)
        logger.info("Database tables created")
    
    def add_task_record(self, task_type, query, status='pending'):
        """
        Add a new task record
        
        Args:
            task_type: Type of task (code, image, research, etc.)
            query: The query or request
            status: Initial status (default: pending)
            
        Returns:
            The created task record
        """
        try:
            session = Session()
            task_record = TaskRecord(
                task_type=task_type,
                query=query,
                status=status
            )
            session.add(task_record)
            session.commit()
            logger.info(f"Added task record: {task_record.id}")
            return task_record.to_dict()
        except Exception as e:
            logger.error(f"Error adding task record: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def update_task_record(self, task_id, result=None, status=None):
        """
        Update an existing task record
        
        Args:
            task_id: ID of the task to update
            result: Task result (optional)
            status: New status (optional)
            
        Returns:
            The updated task record
        """
        try:
            session = Session()
            task_record = session.query(TaskRecord).filter(TaskRecord.id == task_id).first()
            
            if not task_record:
                logger.error(f"Task record not found: {task_id}")
                return None
            
            if result is not None:
                task_record.result = result
            
            if status is not None:
                task_record.status = status
                if status in ['success', 'error']:
                    task_record.completed_at = datetime.utcnow()
            
            session.commit()
            logger.info(f"Updated task record: {task_id}")
            return task_record.to_dict()
        except Exception as e:
            logger.error(f"Error updating task record: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_task_record(self, task_id):
        """
        Get a task record by ID
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            The task record
        """
        try:
            session = Session()
            task_record = session.query(TaskRecord).filter(TaskRecord.id == task_id).first()
            
            if not task_record:
                logger.error(f"Task record not found: {task_id}")
                return None
            
            return task_record.to_dict()
        except Exception as e:
            logger.error(f"Error getting task record: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_recent_tasks(self, limit=10):
        """
        Get recent task records
        
        Args:
            limit: Maximum number of records to retrieve
            
        Returns:
            List of recent task records
        """
        try:
            session = Session()
            task_records = session.query(TaskRecord).order_by(TaskRecord.created_at.desc()).limit(limit).all()
            return [record.to_dict() for record in task_records]
        except Exception as e:
            logger.error(f"Error getting recent tasks: {str(e)}")
            raise
        finally:
            session.close()
    
    def save_agent_state(self, agent_name, state_data):
        """
        Save agent state
        
        Args:
            agent_name: Name of the agent
            state_data: State data to save (will be JSON serialized)
            
        Returns:
            The saved agent state
        """
        try:
            session = Session()
            agent_state = session.query(AgentState).filter(AgentState.agent_name == agent_name).first()
            
            if agent_state:
                agent_state.state_data = json.dumps(state_data)
                agent_state.updated_at = datetime.utcnow()
            else:
                agent_state = AgentState(
                    agent_name=agent_name,
                    state_data=json.dumps(state_data)
                )
                session.add(agent_state)
            
            session.commit()
            logger.info(f"Saved state for agent: {agent_name}")
            return agent_state.to_dict()
        except Exception as e:
            logger.error(f"Error saving agent state: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_agent_state(self, agent_name):
        """
        Get agent state
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            The agent state or None if not found
        """
        try:
            session = Session()
            agent_state = session.query(AgentState).filter(AgentState.agent_name == agent_name).first()
            
            if not agent_state:
                logger.info(f"No state found for agent: {agent_name}")
                return None
            
            return agent_state.to_dict()
        except Exception as e:
            logger.error(f"Error getting agent state: {str(e)}")
            raise
        finally:
            session.close()
