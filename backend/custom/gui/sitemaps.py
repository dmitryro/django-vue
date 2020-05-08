# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from custom.users.models import AboutUs



class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
       return AboutUs.objects.all

#    def items(self):
#        return ['blog', 'contact', 'services', 'faq', 'frequentlyasked', 'pricing', 'about', 'aboutus']

    def location(self, item):
        return reverse(item)

