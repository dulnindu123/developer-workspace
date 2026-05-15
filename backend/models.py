from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    description = Column(String)
    language = Column(String) # Python, Java, JS, etc.
    status = Column(String, default="pending") # pending, analyzing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="projects")
    classes = relationship("ClassNode", back_populates="project")
    functions = relationship("FunctionNode", back_populates="project")
    dependencies = relationship("DependencyEdge", back_populates="project")

class ClassNode(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    file_path = Column(String)
    name = Column(String)
    start_line = Column(Integer)
    end_line = Column(Integer)

    project = relationship("Project", back_populates="classes")

class FunctionNode(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    file_path = Column(String)
    name = Column(String)
    start_line = Column(Integer)
    end_line = Column(Integer)

    project = relationship("Project", back_populates="functions")

class DependencyEdge(Base):
    __tablename__ = "dependencies"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    source = Column(String) # Class or Function name making the call
    target = Column(String) # Class or Function name being called
    type = Column(String) # e.g. "import", "call", "inheritance"

    project = relationship("Project", back_populates="dependencies")
