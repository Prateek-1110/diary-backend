from django.urls import path
from .views import TimelineListCreateView

urlpatterns = [
    path('', TimelineListCreateView.as_view(), name='timeline-list-create'),
]