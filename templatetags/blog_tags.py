# Use the following line in your project's templates to include the usage of this app
#
# {% load blog_tags %}
#
# What types of tags should we support
#
# {% latest_blog_entry %}

from django import template
from blog.models import Entry, EntryManager
from django.shortcuts import get_object_or_404, get_list_or_404

register = template.Library()

# List Single Entry
@register.inclusion_tag('blogtags/entry_detail.html')
def display_entry(entry):
	return { 'entry' : entry }

# List Latest Entry
@register.inclusion_tag('blogtags/entry_detail.html')
def latest_entry():
	entry = Entry.objects.latest()
	return { 'entry' : entry }

# List the Entire Blog Archive
@register.inclusion_tag('blogtags/blog_archive.html')
def blog_archive():
	years = Entry.objects.get_all_years()
	return { 'years' : years }

# List All Entries In Given Year			
@register.inclusion_tag('blogtags/entry_list.html')
def entry_list_for_year(year):
	entries = get_list_or_404(Entry.objects.published(), date_published__year=year)
	return { 'year' : year, 'entries' : entries }

# A List Of Entries
@register.inclusion_tag('blogtags/entry_list.html')
def entry_list(entries):
	return { 'entries' : entries }
	


