from django.db.models import Q
from  django_filters import CharFilter
from django_filters import rest_framework as filters, DateFromToRangeFilter
from django_filters.rest_framework import FilterSet
from advertisements.models import Advertisement


class AdvertisementDateOrCreatorFilter(FilterSet):
    created_at = DateFromToRangeFilter()
    creator = CharFilter(method='status_creator_filter')
    status = CharFilter(method='status_creator_filter')

    def status_creator_filter(self, queryset, name, value):
        if name == 'status':
            return queryset.filter(Q(status__icontains=value))

        if name == 'creator':
            return queryset.filter(Q(creator__id__icontains=value))


    class Meta:
        model = Advertisement
        fields = ['status', 'creator', 'created_at']