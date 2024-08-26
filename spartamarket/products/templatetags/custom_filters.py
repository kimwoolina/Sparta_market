from django import template

register = template.Library()

@register.filter(name='date_equals')
def date_equals(value1, value2):
    # 날짜를 초 단위까지 비교
    return value1.replace(microsecond=0) == value2.replace(microsecond=0)
