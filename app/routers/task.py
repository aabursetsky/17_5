from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import *
from app.schemas import CreateTask, UpdateTask
# Функция создания slug-строки
from slugify import slugify
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))

    if task is not None:
        return task

    raise HTTPException(
        status_code=404,
        detail="Task was not found"
    )

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], task_create: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))

    if user is None:
        db.execute(insert(Task).values(title=task_create.title,
                                       content=task_create.content,
                                       user_id=user.id,
                                       slug=slugify(task_create.title)))
        db.commit()

        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }

    raise HTTPException(
        status_code=404,
        detail="User was not found"
    )

@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, task_update: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        db.execute(update(Task).where(Task.id == task_id).values(
            title=task_update.title,
            content=task_update.content,
            priority=task_update.priority
        ))
        db.commit()

        return{
           'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful'
        }
    raise HTTPException(
        status_code=404,
        detail="Task was not found"
    )


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))

    if task is not None:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()

        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful'
        }
    raise HTTPException(
        status_code=404,
        detail="Task was not found"
    )
