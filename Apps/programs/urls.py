from django.urls import path
from .views import FacultyList, FacultyDetail, ProgramDetail, ProgramList

urlpatterns = [
    path('', ProgramList.as_view(), name='programs'),  # List of all programs
    path('<int:pk>', ProgramDetail.as_view(), name='program-detail'),  # Details of a specific program
    path('faculties/', FacultyList.as_view(), name='faculty-list'),  # List of all faculties
    path('faculties/<int:pk>', FacultyDetail.as_view(), name='faculty-detail'),  # Details of a specific faculty
]
