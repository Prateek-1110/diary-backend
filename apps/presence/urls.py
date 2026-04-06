from django.urls import path
from .views import PresenceView

urlpatterns = [
    path('', PresenceView.as_view(), name='presence'),
]