from rest_framework import serializers
from .models import TimelineEvent

class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = ['id', 'label', 'source', 'source_id', 'event_date', 'is_milestone']
        read_only_fields = ['id', 'source', 'source_id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['source'] = 'manual'
        return super().create(validated_data)