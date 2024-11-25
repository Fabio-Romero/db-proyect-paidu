from django.urls import path
from .views import UserList, UserDetail, group_users_by_research_group_filtered, users_by_program

# Define the URL patterns for the 'users' application
urlpatterns = [
    # Route for listing all users or creating a new user
    path('', UserList.as_view(), name='user-list'),
    
    # Route for retrieving, updating, or deleting a specific user by their primary key (pk)
    path('<int:pk>', UserDetail.as_view(), name='user-detail'),
    
    # Route for filtering users by program ID
    path('user-program/<int:program_id>/', users_by_program, name='users-by-program'),

    # Route for grouping users by research group with filtering
    path('group-by-research-group-filtered/', group_users_by_research_group_filtered, name='group-users-by-research-group-filtered'),
]