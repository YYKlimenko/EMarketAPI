from time import sleep

from market.tasks.config import app


@app.task
def hello():
    # sleep(100000)
    return '1'