from django.urls import path
from .views import MediaVaultListCreateView, MediaVaultDetailView

urlpatterns = [
    path('', MediaVaultListCreateView.as_view()),
    path('<uuid:pk>/', MediaVaultDetailView.as_view()),
]