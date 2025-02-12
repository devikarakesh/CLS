import os
import multiprocessing
from celery import Celery

# Set multiprocessing start method to 'spawn' (required for Windows)
multiprocessing.set_start_method('spawn', force=True)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectlabschedule.settings')
app = Celery('projectlabschedule')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()