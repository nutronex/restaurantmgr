from django import template

register = template.Library()

@register.filter(name='sum_bill')
def get_total_bill(obj_list):
    return sum( [i['p']*i['q'] for i in obj_list] )

