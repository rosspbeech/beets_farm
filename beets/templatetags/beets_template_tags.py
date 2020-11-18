from django import template
from beets.models import Persona

register = template.Library()


@register.inclusion_tag('beets/personas.html')
def get_persona_list(current_persona=None):
    return {'personas': Persona.objects.all(),
            'current_persona': current_persona}
