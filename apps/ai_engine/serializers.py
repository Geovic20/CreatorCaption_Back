from rest_framework import serializers
from .models import CaptionGeneration

class CaptionGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaptionGeneration
        fields = ["id", "topic", "platform", "tone", "created_at"]
        read_only_fields = ("id", "created_at")
