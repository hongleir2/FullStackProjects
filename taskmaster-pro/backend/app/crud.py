import logging
from datetime import timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
from .kafka_producer import send_notification
from .elasticsearch_client import index_task

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# The CryptContext class is used to create a context object that manages the hashing and verification of passwords.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# The get_user() function is used to retrieve a user from the database based on their user ID.
# It takes a database session and a user ID as input, and returns the User object if found.
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# The get_user_by_email() function is used to retrieve a user from the database based on their email address.
# It takes a database session and an email address as input, and returns the User object if found.
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# The create_user() function is used to create a new user in the database.
# It takes a database session and a UserCreate object as input, and returns the newly created User object.
def create_user(db: Session, user: schemas.UserCreate):
    
    # The hash() function is used to hash the user's password using the bcrypt hashing algorithm.
    hashed_password = pwd_context.hash(user.password)
    # The User object is created with the email and hashed_password values.
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    
    # The User object is added to the database session and committed to the database.
    db.add(db_user)
    db.commit()
    
    # The refresh() method is called on the User object to ensure that the object is fully loaded from the database.
    db.refresh(db_user)
    return db_user


# The verify_password() function is used to verify a plain text password against a hashed password.
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# The authenticate_user() function is used to authenticate a user based on their email address and password.
def authenticate_user(db: Session, email: str, password: str):

    # Retrieve the user from the database
    user = get_user_by_email(db, email)
    if not user:
        return False

    # Verify the password
    if not verify_password(password, user.hashed_password):
        return False

    logger.info("User authenticated successfully: %s", email)
    return user


# The get_tasks() function is used to retrieve a list of tasks from the database.
def get_tasks(db: Session, skip: int=0, limit: int=100, owner_id: int=None):
    query = db.query(models.Task)
    
    if owner_id:
        query = query.filter(models.Task.owner_id == owner_id)
    
    return query.offset(skip).limit(limit).all()


# The get_task() function is used to retrieve a task from the database based on its task ID.
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


# The create_task() function is used to create a new task in the database.
def create_task(db: Session, task: schemas.TaskCreate, owner_id: int):
    db_task = models.Task(**task.dict(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    index_task(db_task)
    send_notification(owner_id, f"Task '{db_task.title}' created!")
    return db_task


# The update_task() function is used to update a task in the database.
def update_task(db: Session, db_task: models.Task, updates: schemas.TaskUpdate):
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    index_task(db_task)
    send_notification(db_task.owner_id, f"Task '{db_task.title}' updated!")
    return db_task

# The delete_task() function is used to delete a task from the database.
def delete_task(db: Session, db_task: models.Task):
    db.delete(db_task)
    db.commit()
    send_notification(db_task.owner_id, f"Task '{db_task.title}' deleted!")