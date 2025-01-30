import os
from dotenv import load_dotenv
from sqlalchemy import create_engine  # Used to create the database engine instance
from sqlalchemy.ext.declarative import declarative_base  # Used to create declarative base class for models
from sqlalchemy.orm import sessionmaker  # Factory to create database sessions

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# The engine is the starting point for any SQLAlchemy application
# It maintains the pool of database connections and provides the interface to your database

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# sessionmaker creates a factory for database sessions
# autocommit=False: Changes won't be committed automatically
# autoflush=False: Changes won't be flushed automatically
# bind=engine: Associates the session with our database engine

# Create Base class
Base = declarative_base()
# This is the class we inherit from to create database models/tables
# It provides a base for declarative models and maintains a catalog of classes and tables

# Dependency to get DB session
def get_db():
  db = SessionLocal()  # Create a new database session
  try:
    yield db  # Use yield to enable the session to be used as a dependency
    # This makes the session available for dependency injection in FastAPI
  finally:
    db.close()  # Ensure the session is closed after use
    # This is important for cleaning up resources and preventing memory leaks