import rest_framework_filters as filters

from models import Package


class PackageFilter(filters.FilterSet):
    id = filters.CharFilter(name='id')
    title = filters.CharFilter(name='title')
    fees = filters.CharFilter(name='fees')
    price = filters.CharFilter(name='price')
    is_available = filters.BooleanFilter(name='is_available')
    description = filters.CharFilter(name='description')
    state = filters.CharFilter(name='state')
    package_type = filters.CharFilter(name='package_type')

    class Meta:
        model = Package
        fields = ['id', 'title', 'fees', 'price', 
                  'is_available', 'description', 
                  'state', 'package_type', 'notes']


