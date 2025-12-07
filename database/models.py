# Modelli SQLAlchemy per Super Agent
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    tasks = relationship('Task', back_populates='agent')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    type = Column(String)
    status = Column(String)
    result = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    agent = relationship('Agent', back_populates='tasks')

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
