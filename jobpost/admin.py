from django.contrib import admin
from .models import JobPost, Skill

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'client', 'term', 'scope', 'length', 'experience_needed', 'hire_opp', 'project_budget', 'created_time')
    list_filter = ('term', 'scope', 'length', 'experience_needed', 'hire_opp', 'client')
    search_fields = ('job_title', 'description', 'client__user__name', 'client__user__email')
    readonly_fields = ('attachment_preview',)

    def attachment_preview(self, obj):
        if obj.attachment:
            return f'<a href="{obj.attachment.url}" target="_blank">View Attachment</a>'
        return 'No attachment uploaded.'
    
    attachment_preview.short_description = 'Attachment Preview'
    attachment_preview.allow_tags = True

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
