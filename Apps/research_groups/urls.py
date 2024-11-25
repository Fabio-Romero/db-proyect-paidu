from django.urls import path
from .views import ResearchGroupDetail, ResearchGroupList, filter_research_groups_by_technology

urlpatterns = [
    # URL pattern for listing all research groups
    path('', ResearchGroupList.as_view(), name='research-group-list'),
    
    # URL pattern for retrieving, updating, or deleting a specific research group by its primary key (pk)
    path('<int:pk>', ResearchGroupDetail.as_view(), name='research-group-detail'),
    
    # URL pattern for filtering research groups related to new technologies
    path('filter/key-word/', filter_research_groups_by_technology, name='filter-research-groups-by-technology'),
]
