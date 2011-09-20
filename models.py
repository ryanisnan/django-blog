###############################
#          models.py          #
###############################

from django.db import models
from django.contrib.auth.models import User

import datetime

class EntryManager(models.Manager):
	def latest(self):
		return self.published().latest()
	
	def published(self, **kwargs):
		return super(EntryManager, self).get_query_set().filter(status=Entry.PUBLISHED_STATUS, date_published__lte=datetime.datetime.now)
	
	def get_all_years(self, **kwargs):
		return Entry.objects.published().dates('date_published', 'year', order='DESC')
			
# Import django-tagging
from tagging.fields import TagField

class Entry(models.Model):
	
	DRAFT_STATUS = 1
	PUBLISHED_STATUS = 2
	STATUS_CHOICES = (
		(DRAFT_STATUS, 'Draft'),
		(PUBLISHED_STATUS, 'Published')
	)
	
	title = models.CharField(max_length=140, blank=False)
	slug = models.SlugField(unique_for_date='date_published')
	entry_text = models.TextField()
	entry_html = models.TextField(blank=True)
	author = models.ForeignKey(User)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	date_published = models.DateTimeField(default=datetime.datetime.now())
	status = models.SmallIntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS)
	tags = TagField()
	
	objects = EntryManager()

	class Meta:
		get_latest_by = 'date_published'
		ordering = ('-date_published',)
		verbose_name_plural = 'Entries'
		
	def __unicode__(self):
		return self.title
	
	def is_published(self):
		return (self.status == self.PUBLISHED_STATUS and self.date_published <= datetime.datetime.now())
		
	def save(self, force_insert=False, force_update=False):
		from markdown import markdown
		from smartypants import smartyPants
		self.entry_html = markdown(self.entry_text, output_format='html4')
		super(Entry, self).save(force_insert, force_update)

	def get_previous_published_entry(self):
		return self.get_previous_by_date_published(status=self.PUBLISHED_STATUS, date_published__lte=datetime.datetime.now)

	def get_next_published_entry(self):
		return self.get_next_by_date_published(status=self.PUBLISHED_STATUS, date_published__lte=datetime.datetime.now)
	
	@models.permalink
	def get_absolute_url(self):
		return ('blog_entry_detail', (), { 'year' : str(self.date_published.year), 'slug' : self.slug })
