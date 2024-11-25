from django.contrib import admin
from .models import ResearchGroup

@admin.register(ResearchGroup)
class ResearchGroupAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ResearchGroup model.
    """
    list_display = ('id', 'name', 'description')  # Fields visible in the admin panel list view
