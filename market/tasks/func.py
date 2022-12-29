from time import sleep

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def stop_time(seconds):
    sleep(seconds)
    return 'Finished'


result = stop_time.apply_async(args=[100], ignore_result=True)
print('Counting')

