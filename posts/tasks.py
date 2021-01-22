from background_task import background

from posts.services import Parser, create_new_posts


@background
def add_new_posts():
    parser = Parser()
    new_posts = parser.get_new_posts()

    if new_posts:
        create_new_posts(new_posts)
