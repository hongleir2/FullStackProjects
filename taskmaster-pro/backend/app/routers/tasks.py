from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..dependencies import get_db, get_current_user
from ..elasticsearch_client import es

# The APIRouter class is used to create a new router object that can be used to define API routes.
router = APIRouter(
    prefix= "/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


# The read_tasks() function is used to retrieve a list of tasks from the database.
@router.get("/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


# The create_task() function is used to create a new task in the database.
@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_task(db=db, task=task, owner_id=current_user.id)


# The search_tasks() function is used to search for tasks in the database based on a search query.
@router.get("/search", response_model=List[schemas.Task])
def search_tasks(query: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    res = es.search(index="tasks", body={
        "query": {
            "bool": {
                "must": [
                    {"match": {"title": query}},  # Search for title
                    {"term": {"owner_id": current_user.id}}  # Filter by owner_id
                ]
            }
        }
    })
    task_ids = [hit["_source"]["task_id"] for hit in res["hits"]["hits"]]

    return db.query(crud.models.Task).filter(crud.models.Task.id.in_(task_ids)).all()

# The read_task() function is used to retrieve a task from the database based on its task ID.
@router.get("/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


# The update_task() function is used to update a task in the database.
@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id:int, updates: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, db_task=db_task, updates=updates)

# The delete_task() function is used to delete a task from the database based on its task ID.
@router.delete("/{task_id}", response_model=None, status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db=db, db_task=db_task)
    return JSONResponse(content={"message": "Task {task_id} deleted successfully"})

