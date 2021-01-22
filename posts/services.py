import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests.utils import default_headers
from rest_framework.exceptions import ValidationError

from posts.models import Post
from posts.utils import is_query_param_valid


class Parser:
    """ Парсер для поиска новых постов """

    def __init__(self):
        self.url = 'https://news.ycombinator.com/'
        self.db_posts_urls = [post.url for post in Post.objects.all()]

    @staticmethod
    def generate_headers():
        """ Генерация заголовков для url запроса """

        user_agent = UserAgent()
        headers = default_headers()
        headers['User-Agent'] = user_agent.random
        return headers

    def get_item_url(self, item):
        """ Получение ссылки из объекта поста """

        return item['href'] if item['href'].startswith('http') else f'{self.url}{item["href"]}'

    def generate_post_item(self, item):
        """ Генерация поста в формате словаря """

        return {'title': item.text, 'url': self.get_item_url(item)}

    def get_post_items(self, content):
        """ Получение списка постов в формате словаря """

        soup = BeautifulSoup(content, 'lxml')
        posts = soup.find_all('a', class_='storylink')
        return [self.generate_post_item(post) for post in posts]

    def get_url_posts(self):
        """ Отправка запроса и получение списка постов со страницы """

        response = requests.get(self.url, headers=self.generate_headers())
        return self.get_post_items(response.content)

    def get_new_posts(self):
        """ Получение списка новых постов """

        url_posts = self.get_url_posts()
        return [post for post in url_posts if post['url'] not in self.db_posts_urls]


def create_new_posts(posts):
    """ Добавление новых постов в БД """

    new_posts = []
    for post in posts:
        new_posts.append(Post(title=post['title'], url=post['url']))
    return Post.objects.bulk_create(new_posts)


def get_all_posts():
    """ Получение всех постов из БД """

    return Post.objects.all()


def order_queryset_by_param(queryset, ordering, ordering_fields):
    """ Сортировка queryset по заданному полю """

    if ordering.replace('-', '') in ordering_fields:
        return queryset.order_by(ordering)
    else:
        raise ValidationError(f'Сортировка по полю {ordering} невозможна')


def filter_queryset_by_param(param, queryset, value):
    """ Фильтрация queryset по заданному параметру """
    
    if is_query_param_valid(param, value, len(queryset)):
        if param == 'offset':
            return queryset[int(value):]
        if param == 'limit':
            return queryset[:int(value)]
