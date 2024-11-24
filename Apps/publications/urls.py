from django.urls import path
from .views import PublicationList, PublicationDetail

urlpatterns = [
    path('', PublicationList.as_view(), name='publication-list'),  # URL for retrieving and creating publications
    path('<int:pk>', PublicationDetail.as_view(), name='publication-detail'),  # URL for retrieving, updating, partially updating, or deleting a specific publication by its primary key (pk)
]
