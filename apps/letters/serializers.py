from rest_framework import serializers
from django.utils import timezone
from .models import FutureLetter

class FutureLetterSerializer(serializers.ModelSerializer):
    is_locked = serializers.SerializerMethodField()
    seconds_remaining = serializers.SerializerMethodField()

    class Meta:
        model = FutureLetter
        fields = [
            'id', 'subject', 'unlocks_at', 'is_unlocked',
            'opened_at', 'created_at', 'is_locked', 'seconds_remaining',
        ]
        read_only_fields = ['id', 'is_unlocked', 'opened_at', 'created_at']

    def get_is_locked(self, obj):
        return timezone.now() < obj.unlocks_at

    def get_seconds_remaining(self, obj):
        delta = obj.unlocks_at - timezone.now()
        return max(0, int(delta.total_seconds()))


class FutureLetterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FutureLetter
        fields = ['id', 'subject', 'body', 'unlocks_at']
        read_only_fields = ['id']

    def validate_unlocks_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("unlocks_at must be in the future.")
        return value


class FutureLetterDetailSerializer(serializers.ModelSerializer):
    is_locked = serializers.SerializerMethodField()
    seconds_remaining = serializers.SerializerMethodField()

    class Meta:
        model = FutureLetter
        fields = [
            'id', 'subject', 'body', 'unlocks_at', 'is_unlocked',
            'opened_at', 'created_at', 'is_locked', 'seconds_remaining',
        ]
        read_only_fields = ['id', 'is_unlocked', 'opened_at', 'created_at']

    def get_is_locked(self, obj):
        return timezone.now() < obj.unlocks_at

    def get_seconds_remaining(self, obj):
        delta = obj.unlocks_at - timezone.now()
        return max(0, int(delta.total_seconds()))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # If still locked, scrub the body
        if data['is_locked']:
            data.pop('body')
        return data