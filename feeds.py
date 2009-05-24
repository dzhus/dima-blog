# -*- coding: utf-8 -*-

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from blog.models import Entry
from tagging.models import Tag, TaggedItem

def make_count(bits, default_count=50):
    """
    Return items count from URL bits if last bit is positive integer.
    
    >>> make_count(['Emacs'])
    50
    >>> make_count(['20'])
    20
    >>> make_count(['бред', '15'])
    15
    """
    count = default_count
    if len(bits) > 0:
        last_bit = bits[len(bits)-1]
        if last_bit.isdigit():
            count = int(last_bit)
    return count

class GeneralFeed(Feed):
    link = '/blog/'
    feed_type = Atom1Feed
    author_name = 'Дмитрий Джус'
    author_email = 'dima@sphinx.net.ru'
    author_link = '/author/'
    description_template = 'feed_entry_description.html'

    def item_pubdate(self, item):
        return item.add_date
    
class BlogFeed(GeneralFeed):
    """
    Feed of all blog items.
    """
    title = u'Блог Димы Джуса'
    
    def items(self, obj):
        return obj[0].filter(private=0)[:obj[1]]

    def get_object(self, bits):
        count = make_count(bits)
        return (Entry.objects, count)

class BlogTagFeed(BlogFeed):
    """
    Feed of blog items with specific tags.

    Underscore signs in tags are replaced with space.
    """
    def link(self, obj):
        return u'/blog/tag/%s/' % obj[0].name

    def items(self, obj):
        objects = TaggedItem.objects.get_by_model(Entry, obj[0])
        return objects.filter(private=0)[:obj[1]]

    def title(self, obj):
        return u'Блог Димы Джуса: %s' % obj[0].name

    def get_object(self, bits):
        """
        Return tuple of Tag object and requested item count.
        """
        if len(bits) < 1:
            raise ObjectDoesNotExist
        count = make_count(bits)
        tag_name = '/'.join(bits[:-1]).replace('_', ' ')
        return (Tag.objects.get(name=tag_name), count)


