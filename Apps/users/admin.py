from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the User model.
    """
    list_display = ('id', 'first_name', 'last_name', 'email', 'program', 'user_type')
    # Fields visible in the admin panel list view.

    search_fields = ('first_name', 'last_name', 'email', 'program__name')
    # Enables search functionality by first name, last name, email, and program name.

    list_filter = ('user_type', 'program')
    # Adds filters for user type and associated program.

    ordering = ('last_name', 'first_name')
    # Orders the list by last name and then first name.

    list_per_page = 25
    # Displays 25 records per page in the list view.

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'program', 'user_type')
        }),
    )
    # Groups fields in the edit form for better organization.
