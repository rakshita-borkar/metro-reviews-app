from django.urls import path
from . import views

urlpatterns = [
    path('stations/', views.station_list, name='station-list'),
    path('stations/<int:station_id>/', views.station_detail, name='station-detail'),
    path('reviews/create/', views.create_review, name='create-review'),
    path('reviews/recent/', views.recent_reviews, name='recent-reviews'),
    path('dashboard/', views.dashboard_analytics, name='dashboard-analytics'),
    path('reviews/<int:review_id>/helpful/', views.mark_review_helpful, name='mark-helpful'),
    path('stations/search/', views.search_stations, name='search-stations'),
]
