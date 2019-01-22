from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe


class NoneWidget(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return ''
