from django.contrib import admin
from .models import work, Project, Skill, Tag

@admin.register(work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('Seller', 'text')
    search_fields = ('Seller__user__name', 'Seller__user__email')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('Seller', 'title')
    search_fields = ('Seller__user__name', 'Seller__user__email')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('Project', 'name')
    search_fields = ('Project__title',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('Project', 'name')
    search_fields = ('Project__title',)
