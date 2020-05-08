import rest_framework_filters as filters

from models import Address


class AddressFilter(filters.FilterSet):
    id = filters.CharFilter(name='id')
    name_or_company = filters.CharFilter(name='name_or_company')
    city = filters.CharFilter(name='city')
    user_id = filters.CharFilter(name='user_id')
    nickname = filters.CharFilter(name='nickname')
    country = filters.CharFilter(name='country')

    class Meta:
        model = Address
        fields = ['id', 'city', 'name_or_company', 'user_id', 'nickname', 'country']


