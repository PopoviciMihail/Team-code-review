from typing import List, Optional, Dict
from schemas import Task, TaskUpdate, TaskCreate
from database import TaskModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload



async def get_all_tasks_db(db: AsyncSession) -> List[TaskModel]:
    stmt = select(TaskModel).order_by(TaskModel.id)
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def get_task_by_id_db(db: AsyncSession, task_id: int) -> Optional[TaskModel]:
    task = await db.get(TaskModel, task_id)
    return task

async def get_all_completed_tasks(db:AsyncSession) -> List[TaskModel]:
    stmt=select(TaskModel).where(TaskModel.completed== True)
    result= await db.execute(stmt)
    tasks=result.scalars().all()
    return tasks

async def add_task_db(db: AsyncSession, task_data: Dict) -> TaskModel:
    db_task = TaskModel(**task_data)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task_db(db: AsyncSession, task_id: int, update_data: TaskUpdate) -> Optional[TaskModel]:
    db_task = await db.get(TaskModel, task_id)

    if db_task:
        update_dict = update_data.dict(exclude_unset=True)

        for key, value in update_dict.items():
            setattr(db_task, key, value)

        await db.commit()
        await db.refresh(db_task)
        return db_task

    return None


async def delete_task_db(db: AsyncSession, task_id: int) -> bool:
    db_task = await db.get(TaskModel, task_id)

    if db_task:
        await db.delete(db_task)
        await db.commit()
        return True

    return False

