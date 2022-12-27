from time import sleep

from market.tasks.config import celery


@celery.task
def hello():
    # sleep(100000)
    return '1'