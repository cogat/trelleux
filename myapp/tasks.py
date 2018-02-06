from djangosite.celeryconf import app
from celery.task import periodic_task
from .models import *

@app.task
def power(n):
    """Return 2 to the n'th power"""
    return 2 ** n


@periodic_task(run_every=crontab(minute=30)) # on the 30th minute of every hour
def still_here():
    print("I'm still here")
