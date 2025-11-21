from django import template
from ..models import MissionRecord

register = template.Library()

@register.simple_tag()
def latest_missions(limit=3):
    return MissionRecord.objects.order_by('-date', '-time')[:limit]