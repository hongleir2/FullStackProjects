from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .secrets.db_secret import get_secret

# The get_secret function is used to retrieve the secrets from AWS Secrets Manager.
db_secrets = get_secret()

# The DATABASE_URL environment variable is used to connect to the database.
DATABASE_URL = f"postgresql://{db_secrets['username']}:{db_secrets['password']}@{db_secrets['host']}:{db_secrets['port']}/{db_secrets['dbInstanceIdentifier']}"

# The create_engine function is used to create a new database engine.
engine = create_engine(DATABASE_URL)

# The sessionmaker class is a factory for making session objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Base is a class that will be used to create all the tables in the database. 
# It is a base class for all the models in the application. 

if __name__ == "__main__":
    try:
        print("Secret successfully retrieved.", DATABASE_URL)
    except Exception as e:
        print("Failed to retrieve the secret:", e)