from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe
import uuid
from dictionaries.models import Organization


class OrganizationWidget(Widget):
    template_name = 'dictionaries/organization_widget.html'

    def get_context(self, name, value, attrs=None):
        text = ''
        try:
            text = Organization.objects.get(id=value)
        except Organization.DoesNotExist:
            value = ''
        return {'widget': {
            'name': name,
            'value': value,
            'text': text,
        },
            'uid': uuid.uuid1().hex}

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

