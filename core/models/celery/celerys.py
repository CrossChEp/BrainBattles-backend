from celery import Celery


app = Celery(
    'celery',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['celery.tasks']
)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True
)
