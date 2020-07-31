from django import template

register = template.Library()


@register.filter
def str_month(date_time):
    return date_time.strftime("%b")


@register.filter
def cart_total_price(cart):
    if len(cart) == 0:
        return 0
    else:
        total_price = sum(list(map(lambda x: x.course.price, cart)))
        return total_price


@register.filter
def cart_total_quantity(cart):
    return len(cart)
