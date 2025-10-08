from sqlalchemy import Column, String, JSON, DateTime, Text, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    brief = Column(Text, nullable=False)
    tech_stack = Column(JSON)
    wireframes = Column(JSON)
    compliances = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    requirements = relationship("Requirement", back_populates="project")
    test_cases = relationship("TestCase", back_populates="project")
    bugs = relationship("Bug", back_populates="project")

class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    source_type = Column(String)  # 'user_story', 'file', 'jira', 'ado'
    source_id = Column(String)
    title = Column(String)
    description = Column(Text)
    acceptance_criteria = Column(JSON)
    analysis_results = Column(JSON)  # Stores clarity, completeness, risks, etc.
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="requirements")
    test_cases = relationship("TestCase", back_populates="requirement")
    history = relationship("RequirementHistory", back_populates="requirement")

class RequirementHistory(Base):
    __tablename__ = "requirement_history"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    requirement_id = Column(String, ForeignKey("requirements.id"))
    version = Column(Integer)
    changes = Column(JSON)
    changed_by = Column(String)
    changed_at = Column(DateTime, default=datetime.utcnow)
    
    requirement = relationship("Requirement", back_populates="history")

class TestCase(Base):
    __tablename__ = "test_cases"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    requirement_id = Column(String, ForeignKey("requirements.id"))
    test_type = Column(String)  # 'functional', 'non_functional', 'api', 'ui', 'ux'
    category = Column(String)  # 'performance', 'security', 'usability', etc.
    title = Column(String)
    description = Column(Text)
    preconditions = Column(JSON)
    test_steps = Column(JSON)
    expected_results = Column(JSON)
    test_data = Column(JSON)
    priority = Column(String)  # 'critical', 'high', 'medium', 'low'
    tags = Column(JSON)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    project = relationship("Project", back_populates="test_cases")
    requirement = relationship("Requirement", back_populates="test_cases")

class Bug(Base):
    __tablename__ = "bugs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    external_id = Column(String)  # From Jira/ADO
    title = Column(String)
    description = Column(Text)
    module = Column(String)
    bug_type = Column(String)  # 'functional', 'non_functional', 'ui'
    severity = Column(String)  # 'critical', 'major', 'minor', 'trivial'
    priority = Column(String)  # 'p1', 'p2', 'p3', 'p4'
    status = Column(String)
    test_cases_impacted = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="bugs")

class AgentIO(Base):
    __tablename__ = "agent_io"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    agent_name = Column(String)
    input_data = Column(JSON)
    output_data = Column(JSON)
    execution_time = Column(Integer)  # in milliseconds
    status = Column(String)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)