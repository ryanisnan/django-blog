from django.contrib import admin
from blog.models import Entry

class EntryAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_published'
	exclude = ('entry_html',)
	list_display = ('title', 'date_published', 'status', 'author')
	list_filter = ('date_published', 'status', 'author')
	prepopulated_fields = { 'slug' : ('title',) }
	radio_fields = { 'status' : admin.HORIZONTAL }
	search_fields =  ('title', 'entry_text')
	
	def change_view(self, request, object_id, extra_context=None):
		entry = Entry.objects.get(id=object_id)
		preview_url = entry.get_absolute_url() + 'preview/'
		entry_is_published = entry.is_published()
		new_context = {
			'preview_url' : preview_url,
			'entry_is_published' : entry_is_published,
		}
		return super(EntryAdmin, self).change_view(request, object_id, extra_context=new_context)

admin.site.register(Entry, EntryAdmin)