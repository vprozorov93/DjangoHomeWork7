from django.db.models import Q
from  django_filters import CharFilter
from django_filters import rest_framework as filters, DateFromToRangeFilter
from django_filters.rest_framework import FilterSet
from advertisements.models import Advertisement


class AdvertisementDateOrCreatorFilter(FilterSet):
    created_at = DateFromToRangeFilter()
    creator = CharFilter(method='creator_filter')

    def creator_filter(self, queryset, name, value):
        return queryset.filter(Q(creator__id__icontains=value))

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at']