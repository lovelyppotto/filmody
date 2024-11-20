from django.urls import path
from . import views

urlpatterns = [
    path('', views.playlist_view),
    path('<int:playlist_id>/', views.playlist_detail_view),
    path('<int:playlist_id>/videos/', views.playlist_video_view),
    path('<int:playlist_id>/reviews/', views.review_manage),
    path('<int:playlist_id>/like/', views.playlist_toggle_like),
    path('<int:playlist_id>/review-list/', views.playlist_reviews),
    path('<int:playlist_id>/videos/<int:video_id>', views.delete_video),
]
