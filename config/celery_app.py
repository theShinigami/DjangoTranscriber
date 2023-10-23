import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("dj_transcriber")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# backend redis ttl
app.conf.result_expires = 1800

# time limits
app.conf.update(task_soft_time_limit=300, task_time_limit=300)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
