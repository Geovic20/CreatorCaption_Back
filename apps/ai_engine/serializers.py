from rest_framework import serializers
from .models import CaptionGeneration


class CaptionGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaptionGeneration
        fields = "__all__"
        read_only_fields = ("user", "results", "created_at")
