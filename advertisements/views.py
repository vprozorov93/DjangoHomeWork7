from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementDateOrCreatorFilter
from advertisements.models import Advertisement, UserFavoriteAdvertisement
from advertisements.permissions import IsOwnerOrReadOnly, IsDraft
from advertisements.serializers import AdvertisementSerializer, UserFavoriteAdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_class = AdvertisementDateOrCreatorFilter

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

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "list"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update"]:
            return [False]
        elif self.action in ["destroy", "retrieve"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().list(self, request, *args, **kwargs)

        queryset = self.filter_queryset(self.get_queryset()).filter(Q(like_user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
