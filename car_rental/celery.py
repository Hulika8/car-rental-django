import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_rental.settings")

app = Celery("car_rental")

# Load settings from Django settings, with CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all apps
app.autodiscover_tasks()