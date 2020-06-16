from django import template

register = template.Library()


@register.filter
def str_month(date_time):
    return date_time.strftime("%b")
