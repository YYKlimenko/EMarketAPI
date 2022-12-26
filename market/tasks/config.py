from celery import Celery

app = Celery('mailing')
app.conf.broker_url = 'redis://localhost:6379/'
app.conf.result_backend = 'redis://localhost:6379/'
app.conf.result_backend_transport_options = {
    'retry_policy': {
       'timeout': 5.0
    }
}

