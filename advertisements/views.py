from django.db.models import Q
from django.contrib.auth.models import User
from django_filters import DateFromToRangeFilter, NumberFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement, UserFavoriteAdvertisement
from advertisements.permissions import IsOwnerOrReadOnly, IsDraft
from advertisements.serializers import AdvertisementSerializer, UserFavoriteAdvertisementSerializer


class AdvertisementDateFilter(FilterSet):
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['created_at']


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_class = AdvertisementDateFilter

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action in ["retrieve"]:
            return [IsDraft()]
        return []

    def list(self, request, *args, **kwargs):
        if isinstance(request.user, User):
            queryset = self.filter_queryset(self.get_queryset()).filter((Q(status='OPEN') |
                                                                         Q(status='CLOSED')) |
                                                                        Q(status='DRAFT') & Q(creator=request.user))
        else:
            queryset = self.filter_queryset(self.get_queryset()).filter(Q(status='OPEN') | Q(status='CLOSED'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class FavoriteViewSet(ModelViewSet):
    queryset = UserFavoriteAdvertisement.objects.all()
    serializer_class = UserFavoriteAdvertisementSerializer
    filter_backends = [DjangoFilterBackend]

    # def get_permissions(self):
    #     """Получение прав для действий."""
    #     if self.action in ["create"]:
    #         return [IsAuthenticated()]
    #     elif self.action in ["update", "partial_update"]:
    #         return [False]
    #     elif self.action["destroy", "retrieve"]:
    #         return [IsAuthenticated()]
    #     return []

    def destroy(self, request, *args, **kwargs):
        # print(self, request)
        pass
