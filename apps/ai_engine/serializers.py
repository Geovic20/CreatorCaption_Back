from rest_framework import serializers
from .models import CaptionGeneration

class CaptionGenerationSerializer(serializers.ModelSerializer):
    length = serializers.CharField(required=False, allow_blank=True, default="medium")
    cta = serializers.CharField(required=False, allow_blank=True, default="")

    class Meta:
        model = CaptionGeneration
        fields = ["id", "topic", "platform", "tone", "length", "cta", "created_at"]
        read_only_fields = ("id", "created_at")

