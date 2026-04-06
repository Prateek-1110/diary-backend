import uuid
from django.db import models
from django.conf import settings

class MediaVault(models.Model):

    MEDIA_TYPE_CHOICES = [('image', 'Image'), ('audio', 'Audio')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vault_items')

    # OLD: file = models.FileField(upload_to='vault/%Y/%m/')
    # NEW: we store the Supabase public URL instead of a local file
    file_url = models.URLField(max_length=500, blank=True)

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    category = models.CharField(max_length=100, blank=True)
    caption = models.TextField(blank=True)
    unlocks_at = models.DateTimeField(null=True, blank=True, db_index=True)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']