import rest_framework_filters as filters

from models import Service


class ServiceFilter(filters.FilterSet):
    id = filters.CharFilter(name='id')
    title = filters.CharFilter(name='name_or_company')
    statement = filters.CharFilter(name='city')
    time_published = filters.CharFilter(name='user_id')
    description = filters.CharFilter(name='nickname')

    class Meta:
        model = Service
        fields = ['id', 'title', 'statement', 'time_published', 'description',]
