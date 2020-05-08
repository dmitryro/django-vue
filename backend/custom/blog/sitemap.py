from django.contrib.sitemaps import Sitemap
from custom.blog.models import Post, Comment
from django.core.urlresolvers import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return []

class CommentsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
       return Comment.objects.filter(is_published=True)


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
       return Post.objects.filter(is_published=True)
