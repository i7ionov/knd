from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe
import uuid


class AddressListWidget(Widget):
    template_name = 'dictionaries/address_list_widget.html'

    def get_context(self, name, value, attrs=None):
        return {'widget': {
            'name': name,
            'value': value,
        },
            'uid': uuid.uuid1().hex}

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)

    def value_from_datadict(self, data, files, name):
        """Это из базового виджета MultipleSelect. Нужна для корректного сохранения значения виджета."""
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)

