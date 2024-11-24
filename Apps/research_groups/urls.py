from django.urls import path
from .views import ResearchGroupDetail, ResearchGroupList

urlpatterns = [
    # URL pattern for listing all research groups
    path('', ResearchGroupList.as_view(), name='research-group-list'),
    # URL pattern for retrieving, updating, or deleting a specific research group by its primary key (pk)
    path('<int:pk>', ResearchGroupDetail.as_view(), name='research-group-detail'),
]
