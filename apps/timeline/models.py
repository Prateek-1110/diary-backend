import uuid
from django.db import models
from django.conf import settings

class TimelineEvent(models.Model):
    SOURCE_CHOICES = [
        ('manual', 'Manual'),
        ('diary', 'Diary'),
        ('letter', 'Letter'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timeline_events')
    label = models.CharField(max_length=255)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='manual')
    source_id = models.UUIDField(null=True, blank=True)
    event_date = models.DateField(db_index=True)
    is_milestone = models.BooleanField(default=False)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return f"{self.label} ({self.event_date})"