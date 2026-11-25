from django import forms


class CommaIntegerField(forms.IntegerField):
	def to_python(self, value):
		if isinstance(value, str):
			value = value.replace(',', '').strip()
		return super().to_python(value)


class CurrencyTextInput(forms.TextInput):
	def __init__(self, attrs=None):
		widget_attrs = {
			'data-currency-input': 'true',
			'inputmode': 'numeric',
		}
		widget_attrs.update(attrs or {})
		super().__init__(attrs=widget_attrs)


def mark_browser_local_defaults(form, field_names, clear_initial=()):
	if form.is_bound:
		return

	for field_name in field_names:
		if field_name not in form.fields:
			continue

		if field_name in clear_initial and not getattr(form.instance, 'pk', None):
			form.initial[field_name] = ''

		form.fields[field_name].widget.attrs['data-local-current'] = field_name
