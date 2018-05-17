from django.core.management.base import BaseCommand, CommandError

from trelleux import tasks


class Command(BaseCommand):
    help = 'Run a task'

    def add_arguments(self, parser):
        parser.add_argument('task_name')

    def handle(self, *args, **options):
        getattr(tasks, options['task_name'])()
