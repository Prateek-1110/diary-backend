from rest_framework import serializers
from .models import DiaryEntry, MOOD_CHOICES

class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryEntry
        fields = [
            'id', 'title', 'body', 'mood', 'visibility',
            'theme_override', 'font_override', 'is_pinned',
            'written_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_mood(self, value):
        if value and value not in MOOD_CHOICES:
            raise serializers.ValidationError(f"mood must be one of {MOOD_CHOICES}")
        return value

    def validate_visibility(self, value):
        if value not in ['private', 'shared']:
            raise serializers.ValidationError("visibility must be 'private' or 'shared'")
        return value