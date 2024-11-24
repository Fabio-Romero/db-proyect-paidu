from django.urls import path
from .views import UserList, UserDetail

# Define the URL patterns for the 'users' application
urlpatterns = [
    # Route for listing all users or creating a new user
    path('', UserList.as_view(), name='user-list'),
    
    # Route for retrieving, updating, or deleting a specific user by their primary key (pk)
    path('<int:pk>', UserDetail.as_view(), name='user-detail'),
]
