from django.urls import path
from .views import PublicationList, PublicationDetail, filter_publications_by_date_and_faculty, filter_publications_by_word_date, group_publications_by_research_group, group_publications_by_user_and_research_group

urlpatterns = [
    # URL for retrieving and creating publications
    path('', PublicationList.as_view(), name='publication-list'),  
    
    # URL for retrieving, updating, partially updating, or deleting a specific publication by primary key (pk)
    path('<int:pk>', PublicationDetail.as_view(), name='publication-detail'),  
    
    # URL to filter publications by word and date
    path('filter/word-date/', filter_publications_by_word_date, name='filter-publications'),  
    
    # URL to filter publications by date and faculty
    path('filter/date-faculty/', filter_publications_by_date_and_faculty, name='filter-publications-by-date-and-faculty'),  
    
    # URL to group publications by research group
    path('count/research-group/', group_publications_by_research_group, name='group-publications-by-research-group'),  
    
    # URL to group publications by user and research group
    path('group-by-user-and-research-group/', group_publications_by_user_and_research_group, name='group-publications-by-user-and-research-group'),
]
