from sqlalchemy import Column, Integer, String, Boolean, DateTime #necessary SQLAlchemy column types and tools used to define a database table.
from datetime import datetime #Python’s built-in datetime module.
from database import Base #This imports the Base class from your database.py.

class Task(Base): #his specifies the name of the table in the database.
    __tablename__ = "tasks"  # the actual SQL table name  
 
    id = Column(Integer, primary_key=True, index=True) # Acts as a unique identifier for each task
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


    