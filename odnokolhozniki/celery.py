import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odnokolhozniki.settings')
app = Celery('odnokolhozniki')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()