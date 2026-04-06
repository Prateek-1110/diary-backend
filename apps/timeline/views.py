from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import TimelineEvent
from .serializers import TimelineEventSerializer

class TimelineListCreateView(generics.ListCreateAPIView):
    serializer_class = TimelineEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TimelineEvent.objects.filter(user=self.request.user).order_by('event_date')