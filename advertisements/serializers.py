from collections import OrderedDict

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, UserFavoriteAdvertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'creator',
                  'status', 'created_at', ]
        read_only_fields = ['creator', ]

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if data.get('status') == 'OPEN':
            if Advertisement.objects.filter(creator=self.context['request'].user, status='OPEN').count() >= 10:
                raise ValidationError('Превышен лимит открытых объявлений')

        return data


class UserFavoriteAdvertisementSerializer(serializers.ModelSerializer):
    like_user = UserSerializer(read_only=True)
    advertisement = AdvertisementSerializer(read_only=True)

    class Meta:
        model = UserFavoriteAdvertisement
        fields = ['id', 'advertisement', 'like_user']
        read_only_fields = ['like_user', 'advertisement']

    def validate(self, data):
        request_user = self.context['request'].user
        request_adv = Advertisement.objects.filter(id=self.context['request'].data['advertisement'])

        if request_adv.count() != 1:
            raise ValidationError('Объявление не найдено')
        if UserFavoriteAdvertisement.objects.filter(like_user=request_user, advertisement=request_adv[0]).count() > 0:
            raise ValidationError('Уже добавлено в избранное')
        if request_user == request_adv[0].creator:
            raise ValidationError('Пользователь не может добавть свое объявление в избранное')

        return OrderedDict([('like_user', request_user), ('advertisement', request_adv[0])])
