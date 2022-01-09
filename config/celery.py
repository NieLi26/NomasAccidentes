import os
from django.conf import settings
from celery.schedules import crontab

from celery import Celery
from celery.app.utils import Settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task
def print_hello():
    print('hola')


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

## Preconfiguracion de tareas periodicas
app.conf.beat_schedule = {
    'Alerta_capacitacion': {
        'task': 'send_notification',
        # 'schedule': crontab(minute='*/1')
        'schedule': crontab(minute=43, hour=22)
    },
    'alertas_actividades': {
        'task': 'send_email_actividad',
        'schedule': crontab(minute='*/1')
        # 'schedule': crontab(minute=43, hour=22)
    }
}

# app.conf.timezone = 'America/Buenos_Aires'
