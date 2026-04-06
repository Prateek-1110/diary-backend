from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import DiaryEntry
from .serializers import DiaryEntrySerializer

class DiaryEntryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DiaryEntrySerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        qs = DiaryEntry.objects.filter(user=self.request.user)
        mood = self.request.query_params.get('mood')
        visibility = self.request.query_params.get('visibility')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if mood:
            qs = qs.filter(mood=mood)
        if visibility:
            qs = qs.filter(visibility=visibility)
        if date_from:
            qs = qs.filter(written_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(written_at__date__lte=date_to)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='memory')
    def memory(self, request):
        today = timezone.localdate()
        entries = DiaryEntry.objects.filter(
            user=request.user,
            written_at__month=today.month,
            written_at__day=today.day,
            written_at__year__lt=today.year
        ).order_by('-written_at')
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)