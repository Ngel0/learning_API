from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# Filter for displaying decimal digits of coin prices
@register.filter
def decimal_digits_format(value):
    str_value = str(value)
    if '.' not in str_value:
        return value
    if str_value[0] != '0':
        return '{:.2f}'.format(value)
    number_of_decimal_digits = 4
    index = str_value.index('.')
    while True:
        if str_value[index + 1] == '0':
            number_of_decimal_digits += 1
            index += 1
        else:
            break
    str_value = '{:.{}f}'.format(value, number_of_decimal_digits)
    return str_value


# Adds commas by thousand
@register.filter
def add_commas(value):
    str_value = str(value)
    if '.' not in str_value:
        return value
    if float(value) < 1000:
        return value
    integer_part, decimal_part = str_value.split('.')
    integer_part = integer_part[::-1]
    integer_part_with_commas = ','.join([integer_part[i:i + 3] for i in range(0, len(integer_part), 3)])
    integer_part_with_commas = integer_part_with_commas[::-1]
    return f'{integer_part_with_commas}.{decimal_part}'


@register.filter
def percentage_format(value):
    str_value = '{:.2f}'.format(value)
    if str_value[0] == '-':
        return mark_safe(f"<span style='color: red'>&#9662;{str_value[1:]}%</span>")
    else:
        return mark_safe(f"<span style='color: green'>&#9652;{str_value}%</span>")
