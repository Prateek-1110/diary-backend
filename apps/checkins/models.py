import uuid
from django.db import models
from django.conf import settings

class MoodCheckin(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'), ('sad', 'Sad'), ('angry', 'Angry'),
        ('anxious', 'Anxious'), ('confused', 'Confused'), ('calm', 'Calm'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='checkins')
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    score = models.IntegerField()  # 1–5
    note = models.TextField(blank=True)
    checked_in_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-checked_in_at']