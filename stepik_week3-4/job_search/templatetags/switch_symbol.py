from django import template

register = template.Library()


@register.filter
def switch_symbol(text: str, arg: str = ',&•') -> str:
    [prev, new] = arg.split('&')
    new_string = ""
    for char in text:
        if char != prev:
            new_string += char
        else:
            new_string += new
    return new_string
