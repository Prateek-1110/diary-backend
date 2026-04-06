from rest_framework import generics, permissions
from django.utils import timezone
from .models import FutureLetter
from .serializers import (
    FutureLetterSerializer,
    FutureLetterCreateSerializer,
    FutureLetterDetailSerializer,
)

class FutureLetterListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FutureLetter.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FutureLetterCreateSerializer
        return FutureLetterSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FutureLetterDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FutureLetterDetailSerializer

    def get_queryset(self):
        return FutureLetter.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark opened_at the first time they read an unlocked letter
        if timezone.now() >= instance.unlocks_at and not instance.opened_at:
            instance.opened_at = timezone.now()
            instance.is_unlocked = True
            instance.save(update_fields=['opened_at', 'is_unlocked'])
        return super().retrieve(request, *args, **kwargs)