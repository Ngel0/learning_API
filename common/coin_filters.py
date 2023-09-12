from django import template

register = template.Library()
@register.filter
def decimal_digits_format(value):
    if int(value) > 0:
        return "{:.2f}".format(value)
    else:
        number_of_decimal_digits = 4
        str_value = str(value)
        index = str_value.index('.')
        while True:
            if str_value[index + 1] == '0':
                number_of_decimal_digits += 1
                index += 1
            else:
                break
        str_value = "{:.{}f}".format(value, number_of_decimal_digits)
        return str_value

@register.filter
def add_commas(value):
    integer_part, decimal_part = str(value).split('.')
    integer_part = integer_part[::-1]
    integer_part_with_commas = ','.join([integer_part[i:i + 3] for i in range(0, len(integer_part), 3)])
    integer_part_with_commas = integer_part_with_commas[::-1]
    return f'{integer_part_with_commas}.{decimal_part}'
