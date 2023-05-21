import os, sys
from celery import Celery
from config.production_settings import INSTALLED_APPS
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.production_settings")

app = Celery("Ecommerce")

app.config_from_object("django.conf:settings")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(INSTALLED_APPS)



app.conf.beat_schedule = {
    'queue_update_task': {
        'task': 'Ecommerce.tasks.is_registered_before_two_months',
       "schedule": crontab(hour=0, minute=0),  # Runs daily at midnight
        'args': ()
    },
}
app.conf.timezone = 'Asia/Kolkata'
