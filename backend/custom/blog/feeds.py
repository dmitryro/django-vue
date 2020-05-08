from django.contrib.syndication.views import Feed
from django.utils import feedgenerator
from custom.blog.models import Post
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
import datetime

class RssSiteNewsFeed(Feed):
    title = "Divorces U.S. Feed"
    link = "/blog/"
    description = "Updates to Divorces U.S. blog."

    def items(self):
        return Post.objects.order_by('-time_published')[:5]

  #  def link(self, obj):
  #      return obj.get_absolute_url()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    # item_link is only needed if NewsItem has no get_absolute_url method.
#    def item_link(self, item):
#        return reverse('posts', args=[item.pk])


class AtomSiteNewsFeed(RssSiteNewsFeed):
    feed_type = Atom1Feed
    subtitle = RssSiteNewsFeed.description

