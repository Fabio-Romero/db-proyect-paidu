from django.contrib import admin
from .models import Faculty, Program

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    # Configuration for the Faculty model display in the admin panel
    list_display = ('id', 'name')  # Displays the Faculty ID and name
    search_fields = ('name',)      # Enables search functionality by name
    ordering = ('name',)           # Orders the list by name

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    # Configuration for the Program model display in the admin panel
    list_display = ('id', 'name', 'faculty')  # Displays the Program ID, name, and associated faculty
    search_fields = ('name',)                 # Enables search functionality by program name
    list_filter = ('faculty',)                # Adds a filter option by faculty
    ordering = ('name',)                      # Orders the list by program name
