from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext

from blog.models import Entry
from tagging.models import Tag, TaggedItem

from django.contrib.auth.decorators import permission_required

def index(request):
	entries = Entry.objects.published()[:3]
	recent_entries = Entry.objects.published()[:5]	
	context = {
		'entries' : entries,
		'recent_entries' : recent_entries,
	}
	return render_to_response('blog/blog_index.html', context, RequestContext(request))
	
def entries_by_year(request, year):
	entries = get_list_or_404(Entry.objects.published(), date_published__year=year)
	recent_entries = Entry.objects.published()[:5]
	context = {
		'year' : year,
		'entries' : entries,
		'recent_entries' : recent_entries,
	}
	return render_to_response('blog/blog_entries_by_year.html', context, RequestContext(request))

def entry_detail(request, year, slug):
	entry = get_object_or_404(Entry.objects.published(), date_published__year=year, slug=slug)	
	recent_entries = Entry.objects.published().exclude(id=entry.id)[:5]	
	context = {
		'entry' : entry,
		'recent_entries' : recent_entries,
	}
	return render_to_response('blog/blog_entry_detail.html', context, RequestContext(request))
	
def entries_by_tag(request, tag):
	tag = Tag.objects.get(name=tag)
	entries = get_list_or_404(TaggedItem.objects.get_by_model(Entry, tag))
	recent_entries = Entry.objects.published()[:5]
	context = {
		'tag' : tag,
		'entries' : entries,
		'recent_entries' : recent_entries,
	}
	return render_to_response('blog/blog_entries_by_tag.html', context, RequestContext(request))

@permission_required('blog.change_entry', '/admin/')
def entry_preview(request, year, slug):
	entry = get_object_or_404(Entry.objects.filter(status=Entry.DRAFT_STATUS), date_published__year=year, slug=slug)
	context = {
		'entry' : entry,
	}
	return render_to_response('blog/blog_entry_detail.html', context, RequestContext(request))