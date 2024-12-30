from fastapi import FastAPI
from .routers import auth, tasks
from .database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)
