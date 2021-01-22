from django.core.management.base import BaseCommand

from posts.tasks import add_new_posts


class Command(BaseCommand):
    """ Команда для поиска новых постов и добавления их в БД """

    def add_arguments(self, parser):
        parser.add_argument('--repeat', nargs='?', type=int, help='Аргумент задает периодичность задания в секундах')

    def handle(self, *args, **options):
        if options['repeat']:
            add_new_posts(repeat=options['repeat'])
        else:
            add_new_posts.now()
