from django import template
import decimal

register = template.Library()

@register.filter(name="usd")
def usd_format(value):
    """Format value as USD."""
    if isinstance(value, decimal.Decimal):
        return f"${value:,.2f}"
    else:
        return value
