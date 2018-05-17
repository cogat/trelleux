"""
Run the update_lists action on all the Trello Boards.
"""
from djangosite.trelleux.models import TrelloBoard
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        for b in TrelloBoard.objects.filter(enabled=True):
            b.update_lists()
            print "Trello lists are up-to-date"
