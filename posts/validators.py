from rest_framework.exceptions import ValidationError


def validate_ordering(ordering_param, query_params, ordering_fields):
    """ Сортировка списка на основании параметра запроса """

    if ordering_param in query_params:
        order_value = query_params[ordering_param]
        if order_value.replace('-', '') not in ordering_fields:
            raise ValidationError(f'Сортировка по полю {order_value} невозможна')
    return True


def validate_param_value_length(param, value, length, max_length):
    """ Валидация параметра запроса на величину значения """

    if value > length:
        raise ValidationError(f'Значение параметра {param} слишком большое. Максимально допустимое {max_length}')


def valid_limit(limit, max_limit):
    """ Возвращает значение параметра limit, при условии прохождения валидации """

    validate_param_value_length('limit', limit, max_limit, max_limit)
    return limit


def valid_offset(offset, count):
    """ Возвращает значение параметра offset, при условии прохождения валидации """

    validate_param_value_length('offset', offset, count, count - 1)
    if offset == count:
        raise ValidationError(f'Значение параметра offset равно количеству постов. Сдвиг невозможен.')
    return offset


def positive_int_value(string_value, param):
    """ Возвращает значение при условии, что оно положительное число"""

    msg = f'Параметр {param} должен быть положительным числом'

    try:
        value = int(string_value)
    except ValueError:
        raise ValidationError(msg)

    if value < 0:
        raise ValidationError(msg)

    return value
