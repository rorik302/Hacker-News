from rest_framework.filters import OrderingFilter

from posts.validators import validate_ordering


class PostsFilter(OrderingFilter):
    """ Фильтр для сортировки постов """
    
    ordering_fields = ['title', 'id', 'created', 'url']
    ordering_param = 'order'

    def filter_queryset(self, request, queryset, view):
        """ Возвращает отсортированный список постов """

        validate_ordering(self.ordering_param, request.query_params, self.ordering_fields)
        return super(PostsFilter, self).filter_queryset(request, queryset, view)
