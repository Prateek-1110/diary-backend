from django.urls import path
from .views import FutureLetterListCreateView, FutureLetterDetailView

urlpatterns = [
    path('', FutureLetterListCreateView.as_view()),
    path('<uuid:pk>/', FutureLetterDetailView.as_view()),
]