from django import template

register = template.Library()


@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''


@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError, TypeError):
        return ''


@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def total_price_with_discount(price, args):
    """
    args: "quantity,discount_percentage"
    Возвращает итоговую сумму с учетом количества и скидки.
    """
    try:
        quantity_str, discount_str = args.split(',')
        quantity = int(quantity_str)
        discount_percentage = float(discount_str)
        original_price = float(price)
        discount_amount = original_price * (discount_percentage / 100)
        discounted_price = original_price - discount_amount
        total = discounted_price * quantity
        return round(total, 2)
    except (ValueError, ZeroDivisionError, TypeError):
        return ''