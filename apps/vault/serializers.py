from rest_framework import serializers
from django.utils import timezone
from .models import MediaVault

class MediaVaultSerializer(serializers.ModelSerializer):
    is_locked = serializers.SerializerMethodField()
    seconds_remaining = serializers.SerializerMethodField()
    file_url_display = serializers.SerializerMethodField()

    class Meta:
        model = MediaVault
        fields = [
            'id', 'media_type', 'category', 'caption',
            'unlocks_at', 'is_hidden', 'created_at',
            'is_locked', 'seconds_remaining', 'file_url_display',
        ]
        read_only_fields = ['id', 'created_at']

    def get_is_locked(self, obj):
        if obj.unlocks_at is None:
            return False
        return timezone.now() < obj.unlocks_at

    def get_seconds_remaining(self, obj):
        if not obj.unlocks_at:
            return 0
        delta = obj.unlocks_at - timezone.now()
        return max(0, int(delta.total_seconds()))

    def get_file_url_display(self, obj):
        # Scrub URL if locked — same logic as before, just using file_url now
        if self.get_is_locked(obj):
            return None
        return obj.file_url  # direct Supabase URL, no request.build_absolute_uri needed


class MediaVaultUploadSerializer(serializers.ModelSerializer):
    # 'file' is write-only — used for upload, not stored in DB directly
    file = serializers.FileField(write_only=True)

    class Meta:
        model = MediaVault
        fields = ['id', 'file', 'media_type', 'category', 'caption', 'unlocks_at', 'is_hidden']
        read_only_fields = ['id']

    def validate(self, data):
        file = data.get('file')
        media_type = data.get('media_type')
        if file and media_type:
            name = file.name.lower()
            if media_type == 'image' and not any(name.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                raise serializers.ValidationError("File doesn't match media_type=image.")
            if media_type == 'audio' and not any(name.endswith(ext) for ext in ['.mp3', '.wav', '.ogg', '.m4a', '.webm']):
                raise serializers.ValidationError("File doesn't match media_type=audio.")
        return data