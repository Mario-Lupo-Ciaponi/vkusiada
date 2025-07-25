import os
import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vkusiada.settings")

app = Celery("vkusiada")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
