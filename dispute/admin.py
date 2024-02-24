from django.contrib import admin
from .models import Dispute

class DisputeAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'resolved']  # Display these fields in the admin list
    list_filter = ['resolved']  # Add a filter for the 'resolved' field
    search_fields = ['title', 'text']  # Add a search bar for these fields

    # Define which fields are editable in the admin
    readonly_fields = ['title', 'text', 'client', 'jobpost']  # Make these fields read-only

    # Customize how fields are displayed in the admin change form
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'resolved')
        }),
        ('Read-only fields', {
            'fields': ('client', 'jobpost'),
            'classes': ('collapse',)  # Hide this section by default
        })
    )

admin.site.register(Dispute, DisputeAdmin)
