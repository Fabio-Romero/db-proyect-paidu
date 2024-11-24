"""
URL configuration for paidu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define the schema view for Swagger documentation
schema_view = get_schema_view(
   openapi.Info(
      title="PAIDU API",  # Title of the API documentation
      default_version='v1',  # Version of the API
      description="This documentation is made to teach you, how to use our api",  # Description or purpose of the API
   ),
   public=True,  # Indicate that the schema is public and accessible
)

# Define the URL patterns for the application
urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),

    # Include URL configurations from the 'programs' application
    path('programs/', include('Apps.programs.urls')),

    # Include URL configurations from the 'publications' application
    path('publications/', include('Apps.publications.urls')),

    # Include URL configurations from the 'users' application
    path('users/', include('Apps.users.urls')),

    # Include URL configurations from the 'research_groups' application
    path('research-groups/', include('Apps.research_groups.urls')),

    # Path for serving API documentation using ReDoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
