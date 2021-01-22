from rest_framework.exceptions import ValidationError


def is_query_params_valid(params, permitted_params):
    """ Валидация допустимых параметров запроса """

    for param in params:
        if param not in permitted_params:
            raise ValidationError(f'Параметр {param} не допустим')
    return True


def is_value_positive(value, param):
    """ Валидация на положительное значение параметра """

    if value < 0:
        raise ValidationError(f'Параметр {param} должен быть положительным числом')
    return True


def is_length_valid(value, length, param):
    """ Валидация допустимой величины значения параметра """

    if value > length:
        raise ValidationError(
            f'Значение параметра {param} слишком большое. Максимально допустимое {length}')
    return True


def is_query_param_valid(param, value, length):
    """ Валидация параметра запроса """

    try:
        value = int(value)
        if is_value_positive(value, param) and is_length_valid(value, length, param):
            return True
    except ValueError:
        raise ValidationError(f'Параметр {param} должен быть положительным числом')
