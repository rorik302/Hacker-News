from rest_framework.exceptions import ValidationError


def is_query_params_valid(params, permitted_params):
    for param in params:
        if param not in permitted_params:
            raise ValidationError(f'Параметр {param} не допустим')
    return True


def is_query_param_valid(param, value, length):
    try:
        value = int(value)
        if value < 0:
            raise ValidationError(f'Параметр {param} должен быть положительным числом')

        if value > length:
            raise ValidationError(
                f'Значение параметра {param} слишком большое. Максимально допустимое {length}')
        return True
    except ValueError:
        raise ValidationError(f'Параметр {param} должен быть положительным числом')
