# -*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from blog.models import Entry
from tagging.models import Tag, TaggedItem

def make_count(bits, index=0, default_count=50):
    """
    Return items count from URL bits. `index` is the expected number
    position.
    
    >>> make_count(['55'])
    55
    >>> make_count(['Emacs', '20'])
    50
    >>> make_count(['бред', '15'], 1)
    15
    """
    # We assume that item count is the last bit
    if len(bits) == index + 1:
        count = int(bits[index])
        if (count < 1):
            raise ObjectDoesNotExist
    else:
        count = default_count
    return count

class GeneralFeed(Feed):
    link = '/blog/'
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
        count = make_count(bits, 0)
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
        count = make_count(bits, 1)
        tag_name = bits[0].replace('_', ' ')
        return (Tag.objects.get(name=tag_name), count)


