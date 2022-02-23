from django_filters import rest_framework as filters

from profile_.models import Profile


class CharFilterInFilter(filters.CharFilter):
    pass


class LocationFilter(filters.FilterSet):
    location = CharFilterInFilter(field_name='location__location')

    class Meta:
        model = Profile
        fields = ['location']