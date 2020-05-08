# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
from haystack import indexes
from custom.gui.models import Service


class ServiceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Service

##site.register(Service, ServiceIndex)
