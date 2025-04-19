from celery import Celery
from celery.schedules import schedule
from src.config import CELERY_BROKER, CELERY_BACKEND
from redbeat import RedBeatSchedulerEntry
celery = Celery('bot_tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)


@celery.task
def print_every_sec(text: str):
    print('--ok--')


def create_periodic_task(task_name, task_interval):
    try:
        entry = RedBeatSchedulerEntry(task_name, 'src.tasks.task_queue.print_every_sec', task_interval,
                                      kwargs={"text": ''},
                                      app=celery)
    except Exception:
        return 0
    if entry:
        entry.save()
        return entry.name


def cancel_task(task_name):
    try:

        entry = RedBeatSchedulerEntry.from_key(task_name, app=celery)
        print(entry)
        print(entry)
        print(entry)
    except KeyError:
        entry = None
    if entry:
        entry.delete()


# Update schedule to 5 seconds
# RedBeatSchedulerEntry.from_key('redbeat:task_259',  app=celery).schedule = schedule(5)
# print(celery.tasks)
create_periodic_task('my_periodic_task', 3)
# cancel_task('my_periodic_task')
