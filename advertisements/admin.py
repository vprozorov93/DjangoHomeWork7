from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, ModelForm

from advertisements.models import Advertisement, UserFavoriteAdvertisement


class UserFavoriteAdvertisementFormset(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            if form.cleaned_data['advertisement'].creator == form.cleaned_data['like_user']:
                raise ValidationError(f'Нельзя добавить свое объявление в список избранных. '
                                      f'Уберите {form.cleaned_data["advertisement"]} из списка избранных.')
        else:
            return super().clean()


class AdvertisementInline(admin.TabularInline):
    """Use in for User ModelAdmin class"""
    model = Advertisement
    extra = 0


class UserFavoriteAdvertisementInline(admin.TabularInline):
    """Use in for User ModelAdmin class"""
    model = UserFavoriteAdvertisement
    formset = UserFavoriteAdvertisementFormset
    extra = 0


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at']
    readonly_fields = ('created_at', 'updated_at')


class UserFavoriteAdvertisementForm(ModelForm):
    class Meta:
        model = UserFavoriteAdvertisement
        fields = ['id', 'advertisement', 'like_user']

    def clean(self):
        cleaned_data = super(UserFavoriteAdvertisementForm, self).clean()
        if cleaned_data['like_user'] == cleaned_data['advertisement'].creator:
            raise ValidationError('Пользователь не может добавть свое объявление в избранное')
        return cleaned_data


@admin.register(UserFavoriteAdvertisement)
class UserFavoriteAdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'advertisement', 'like_user']
    form = UserFavoriteAdvertisementForm
