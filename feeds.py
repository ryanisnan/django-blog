from django.contrib.syndication.views import Feed
from blog.models import Entry

class LatestEntries(Feed):
	title = "Ryan West's Recent Blog Posts"
	link = "/feeds/"
	description = "Recent posts by Ryan West"
	
	def items(self):
		return Entry.objects.published()[:10]
		
	def item_title(self, item):
		return item.title
		
	def item_description(self, item):
		return item.entry_html
		
	def item_pubdate(self, item):
		return item.date_published