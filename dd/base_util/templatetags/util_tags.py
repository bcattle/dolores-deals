from django import template
from django.contrib.flatpages.models import FlatPage

register = template.Library()

@register.inclusion_tag('tags/footer_links.html')
def footer_links():
	flatpage_list = FlatPage.objects.all()
	return { 'flatpage_list': flatpage_list }