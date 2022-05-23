from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class UserFavoriteAdvertisement(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    like_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранное объявление'
        verbose_name_plural = 'Избранные объявления'

    def __str__(self):
        return f'{self.advertisement} в избранном у {self.like_user}'
