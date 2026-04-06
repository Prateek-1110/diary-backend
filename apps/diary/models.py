import uuid
from django.db import models
from django.conf import settings

MOOD_CHOICES = ['happy', 'sad', 'angry', 'anxious', 'confused', 'calm']
VISIBILITY_CHOICES = [('private', 'Private'), ('shared', 'Shared')]

class DiaryEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diary_entries')
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    mood = models.CharField(max_length=20, blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    theme_override = models.CharField(max_length=50, null=True, blank=True)
    font_override = models.CharField(max_length=50, null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    written_at = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-written_at']

    def __str__(self):
        return self.title or str(self.id)