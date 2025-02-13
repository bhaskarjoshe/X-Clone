import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CoreX.settings")

app = Celery("CoreX")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
