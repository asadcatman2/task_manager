
from sqlalchemy import create_engine # creates conn to my database
from sqlalchemy.ext.declarative import declarative_base # create base class of models
from sqlalchemy.orm import sessionmaker # create sessions to interact with database session is a conversation with data base 

# This is the path to your SQLite file
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# The engine = the actual connection to the DB

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed only for SQLite sqllite normally allows one thread but fastapi needs multiple threads without this app will crash with threading errors 
)

# SessionLocal = a factory that creates DB sessions
#SQLAlchemy uses transaction-based operations  Changes are NOT saved automatically
#If autocommit=True (not recommended)
# Every operation would auto-save
#Hard to control transactions
#Risk of partial/inconsistent data
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # func that returns new db sessions

# Base = parent class for all your DB models
Base = declarative_base() #This is used to create tables (models) Without Base:
#  You cannot define tables in Python



