from celery.schedules import crontab

from djangosite.celeryconf import app
from celery.task import periodic_task

from trelleux.models import TrelloBoard

@periodic_task(run_every=crontab(minute=5)) # on the 30th minute of every hour
def update():
    for b in TrelloBoard.objects.filter(enabled=True):
        b.update_lists()
