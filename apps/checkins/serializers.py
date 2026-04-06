from rest_framework import serializers
from .models import MoodCheckin

class MoodCheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodCheckin
        fields = ['id', 'mood', 'score', 'note', 'checked_in_at']
        read_only_fields = ['id', 'checked_in_at']

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value