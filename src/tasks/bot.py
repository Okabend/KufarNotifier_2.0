from .task_queue import celery, create_periodic_task, cancel_task
from celery.schedules import crontab
from celery.result import AsyncResult
from datetime import timedelta
from loguru import logger
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


@celery.task
def my_periodic_task():
    print("Выполняется периодическая задача")


task = create_periodic_task('my_periodic_task', 3)
print(task)
cancel_task('my_periodic_task')
input('task_name')
