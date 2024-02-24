from django.contrib import admin
from .models import Client, ProfilePicture

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city')
    list_filter = ('country', 'city')
    search_fields = ('user__name', 'user__email', 'city')

@admin.register(ProfilePicture)
class ProfilePictureAdmin(admin.ModelAdmin):
    list_display = ('client', 'profile_picture')
    search_fields = ('client__user__name', 'client__user__email')
    list_filter = ('client__city',)
