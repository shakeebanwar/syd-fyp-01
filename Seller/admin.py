from django.contrib import admin
from .models import Seller, ProfilePicture, Portfolio, Education, Language, Skill

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'personal_website')
    search_fields = ('user__name', 'user__email')

@admin.register(ProfilePicture)
class ProfilePictureAdmin(admin.ModelAdmin):
    list_display = ('seller', 'profile_picture')
    search_fields = ('seller__user__name', 'seller__user__email')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('seller', 'url')
    search_fields = ('seller__user__name', 'seller__user__email')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('seller', 'education', 'from_year', 'to_year')
    search_fields = ('seller__user__name', 'seller__user__email')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('seller', 'name')
    search_fields = ('seller__user__name', 'seller__user__email')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('seller', 'name')
    search_fields = ('seller__user__name', 'seller__user__email')
