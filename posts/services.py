import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests.utils import default_headers

from posts.models import Post


class Parser:
    def __init__(self):
        self.url = 'https://news.ycombinator.com/'
        self.db_posts_urls = [post.url for post in Post.objects.all()]

    @staticmethod
    def generate_headers():
        user_agent = UserAgent()
        headers = default_headers()
        headers['User-Agent'] = user_agent.random
        return headers

    def get_item_url(self, item):
        return item['href'] if item['href'].startswith('http') else f'{self.url}{item["href"]}'

    def generate_post_item(self, item):
        return Post(title=item.text, url=self.get_item_url(item))

    def get_post_items(self, content):
        soup = BeautifulSoup(content, 'lxml')
        posts = soup.find_all('a', class_='storylink')
        return [self.generate_post_item(post) for post in posts]

    def get_url_posts(self):
        response = requests.get(self.url, headers=self.generate_headers())
        return self.get_post_items(response.content)

    def get_new_posts(self):
        url_posts = self.get_url_posts()

        return [post for post in url_posts if post.url not in self.db_posts_urls]


def create_new_posts(posts):
    return Post.objects.bulk_create(posts)
