from rest_framework.generics import ListAPIView

from posts.serializers import PostSerializer
from posts.services import order_queryset_by_param, filter_queryset_by_param, get_all_posts
from posts.utils import is_query_params_valid


class PostView(ListAPIView):
    serializer_class = PostSerializer
    ordering_fields = ['title', 'id', 'created', 'url']
    permitted_params = ['order', 'offset', 'limit']

    def get_queryset(self):
        return get_all_posts()

    def filter_queryset(self, queryset):
        queryset = self.get_queryset()
        query_params = self.request.query_params

        if query_params and is_query_params_valid(query_params, self.permitted_params):
            ordering = query_params.get('order', '')
            if ordering:
                queryset = order_queryset_by_param(queryset, ordering, self.ordering_fields)

            offset = query_params.get('offset', '')
            if offset:
                queryset = filter_queryset_by_param('offset', queryset, offset)

            limit = query_params.get('limit', '')
            if limit:
                queryset = filter_queryset_by_param('limit', queryset, limit)
        else:
            queryset = queryset[:5]

        return queryset
