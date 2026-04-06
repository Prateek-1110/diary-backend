from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'display_name', 'theme', 'font', 'last_seen_at']
        read_only_fields = ['id', 'username', 'last_seen_at']