from celery import Celery
import os
import logging

from celery.schedules import crontab

logger = logging.getLogger(__name__)
current_module = __import__(__name__)

CELERY_CONFIG = {
    'CELERY_BROKER_URL':
        'redis://{}/0'.format(os.environ.get('REDIS_URL', 'localhost:6379')),
    'CELERY_TASK_SERIALIZER': 'json',
}

celery = Celery(__name__, broker=CELERY_CONFIG['CELERY_BROKER_URL'])
celery.conf.update(CELERY_CONFIG)

job = {
    'task': 'my_function',
    'schedule': {'minute': 0, 'hour': 0},
    'args': [2, 3],
    'kwargs': {}
}


def add_to_module(f):
    setattr(current_module, 'tasks_{}__'.format(f.name), f)
    return f


@add_to_module
def my_function(x, y, **kwargs):
    return x + y


def add_task(job):
    logger.info("Adding periodic job: %s", job)
    if not isinstance(job, dict) and 'task' in jobs:
        logger.error("Job {} is ill-formed".format(job))
        return False
    celery.add_periodic_task(
        crontab(**job.get('schedule', {'minute': 0, 'hour': 0})),
        get_from_module(job['task']).s(
            enterprise_id,
            *job.get('args', []),
            **job.get('kwargs', {})
        ),
        name=job.get('name'),
        expires=job.get('expires')
    )
    return True


def get_from_module(f):
    return getattr(current_module, 'tasks_{}__'.format(f))
