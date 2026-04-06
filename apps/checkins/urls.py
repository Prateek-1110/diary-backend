from django.urls import path
from .views import MoodCheckinListCreateView, MoodTrendView

urlpatterns = [
    path('', MoodCheckinListCreateView.as_view()),
    path('trend/', MoodTrendView.as_view()),
]