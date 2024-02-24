from django.contrib import admin
from .models import Course, Video, UserProgress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    readonly_fields = ('file_preview',)

    def file_preview(self, obj):
        if obj.file:
            return f'<a href="{obj.file.url}" target="_blank">View File</a>'
        return 'No file uploaded.'
    
    file_preview.short_description = 'File Preview'
    file_preview.allow_tags = True

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'watched')
    list_filter = ('user', 'video')
