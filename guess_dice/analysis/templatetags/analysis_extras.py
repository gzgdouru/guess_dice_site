from django import template

register = template.Library()


@register.filter(name="valueConvert")
def valueConvert(value):
    return "大" if int(value) > 10 else "小"