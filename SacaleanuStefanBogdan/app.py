from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
import service as task_service
from database import init_db, get_db, TaskModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas import Task, TaskCreate, TaskUpdate

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/tasks", response_model=List[Task])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await task_service.get_all_tasks_db(db)
    return tasks

@app.get("/tasks/completed", response_model=List[Task])
async def read_completed_tasks(db:AsyncSession=Depends(get_db)):
    tasks = await task_service.get_all_completed_tasks(db)
    return tasks
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_new_task(task_data: TaskCreate, db: AsyncSession = Depends(get_db)):
    task_dict = task_data.dict()
    task_dict["created_at"] = datetime.now().isoformat()

    db_task = await task_service.add_task_db(db, task_dict)
    return db_task

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    db_task = await task_service.get_task_by_id_db(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task_endpoint(task_id: int, update_data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    db_task = await task_service.update_task_db(db, task_id, update_data)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(task_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await task_service.delete_task_db(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}