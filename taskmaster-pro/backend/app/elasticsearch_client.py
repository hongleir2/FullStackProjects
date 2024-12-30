import os
from elasticsearch import Elasticsearch

from .schemas import Task
from .models import Task as models_Task
from sqlalchemy.orm import Session

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")

es = Elasticsearch([{"host": ELASTICSEARCH_HOST, "port": 9200, "scheme": "http"}])

def index_task(task: Task):
    # Index the task in Elasticsearch
    es.index(index="tasks", body={
        "task_id": task.id,
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "owner_id": task.owner_id,
        "is_completed": task.is_completed
    })
    print(f"Task indexed: {task}")

def reindex_tasks(db: Session):
    tasks = db.query(models_Task).all()
    for task in tasks:
        index_task(task)
    print("Reindexed all tasks")

def test_elasticsearch_connection():
    if es.ping():
        print("Elasticsearch is connected!")
    else:
        print("Failed to connect to Elasticsearch!")

if __name__ == "__main__":
    test_elasticsearch_connection()
