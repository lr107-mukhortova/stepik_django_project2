from django import template

register = template.Library()


@register.filter
def thous_sep(number: int) -> str:
    number = str(number)
    string_number = ""
    for number, char in enumerate(number[::-1]):
        string_number = char + string_number
        if (number+1) % 3 == 0:
            string_number = " " + string_number
    return string_number
