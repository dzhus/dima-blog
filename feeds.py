# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from blog.models import Entry#, Tag

DEFAULT_COUNT = 50

class GeneralFeed(Feed):
    title = "Блог Джуса"
    link = "/blog/"
    author_email = 'mail@sphinx.net.ru'
    author_link = '/author/'
    description_template = 'feed_entry_description.xhtml'

    def item_pubdate(self, item):
        return item.add_date
    
    def items(self, obj):
        return obj

class BlogFeed(GeneralFeed):
    def items(self):
        return Entry.objects.filter(private=0)[:DEFAULT_COUNT]

    def items(self, obj):
        return obj

    def get_object(self, bits):
        count = bits[0]
        if (count < 1) or (len(bits) != 1):
            raise ObjectDoesNotExist
        return Entry.objects.filter(private=0)[:count]

class BlogTagFeed(GeneralFeed):
    def get_object(self, bits):
        tag = bits[0].replace('_', ' ')
        return Tag.objects.get(value=tag).entry_set.filter(private=0)[:DEFAULT_COUNT]

