from rest_framework.generics import ListAPIView

from posts.filters import PostsFilter
from posts.pagination import PostsPagination
from posts.serializers import PostSerializer
from posts.services import get_all_posts


class PostView(ListAPIView):
    serializer_class = PostSerializer
    queryset = get_all_posts()
    filter_backends = [PostsFilter]
    pagination_class = PostsPagination
