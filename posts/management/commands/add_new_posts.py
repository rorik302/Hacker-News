from django.core.management.base import BaseCommand

from posts.tasks import add_new_posts


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--repeat', nargs='?', type=int)

    def handle(self, *args, **options):
        if options['repeat']:
            add_new_posts(repeat=options['repeat'])
        else:
            add_new_posts.now()
