from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# The DATABASE_URL environment variable is used to connect to the database.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://developers:Harry147@localhost:5432/taskmaster-datadb")

# The create_engine function is used to create a new database engine.
engine = create_engine(DATABASE_URL)

# The sessionmaker class is a factory for making session objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Base is a class that will be used to create all the tables in the database. 
# It is a base class for all the models in the application. 