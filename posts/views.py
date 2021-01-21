from rest_framework.generics import ListAPIView

from posts.models import Post
from posts.serializers import PostSerializer


class PostView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()
