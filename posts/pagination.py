from rest_framework.pagination import LimitOffsetPagination

from posts.validators import positive_int_value, valid_offset, valid_limit


class PostsPagination(LimitOffsetPagination):
    default_limit = 5

    def get_limit(self, request):
        """ Получение лимита постов """

        if self.limit_query_param in request.query_params:
            value = request.query_params[self.limit_query_param]
            return positive_int_value(value, self.limit_query_param)
        return self.default_limit

    def get_offset(self, request):
        """ Получение сдвига параметра offset """

        if self.offset_query_param in request.query_params:
            value = request.query_params[self.offset_query_param]
            return positive_int_value(value, self.offset_query_param)
        return 0

    def paginate_queryset(self, queryset, request, view=None):
        """ Фильтрация queryset на основании параметров запроса """

        self.count = self.get_count(queryset)
        self.offset = valid_offset(self.get_offset(request), self.count)
        self.limit = self.get_limit(request)
        self.request = request

        if self.limit is None:
            return None

        """
        Если параметр limit указан, то вернется заданное количество постов, при условии, 
        что limit не конфликтует с параметром offset.
        """
        if self.limit_query_param in request.query_params:
            self.max_limit = self.count - self.offset if not self.max_limit else self.max_limit
            self.limit = valid_limit(self.limit, self.max_limit)

        return list(queryset[self.offset:self.offset + self.limit])
