from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def slice_lines(value, arg=10):
	"""
	lines = 10
	try:
		lines = int(arg)
	except:
		lines = 10
	"""
	return "\n".join(value.split("\n")[:arg])
