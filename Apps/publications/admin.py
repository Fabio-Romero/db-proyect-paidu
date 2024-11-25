from django.contrib import admin
from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Publication model.
    """
    list_display = ('id', 'title', 'publication_date', 'research_group', 'user')
    # Display these fields in the admin list view.

    search_fields = ('title', 'research_group__name', 'user__username')
    # Enable search by title, research group name, and user username.

    list_filter = ('publication_date', 'research_group')
    # Add filters for publication date and research group.

    ordering = ('-publication_date',)
    # Order publications by most recent date first.

    date_hierarchy = 'publication_date'
    # Adds a date-based drilldown navigation.

    list_select_related = ('research_group', 'user')
    # Optimize queries by selecting related objects.

    fieldsets = (
        (None, {
            'fields': ('title', 'abstract', 'publication_date')
        }),
        ('Relationships', {
            'fields': ('research_group', 'user')
        }),
    )
    # Organize fields into collapsible sections in the admin form.