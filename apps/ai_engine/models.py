from django.db import models
from django.conf import settings

# Modèle pour stocker les générations de légendes
class CaptionGeneration(models.Model):
    PLATFORM_CHOICES = [
        ("tiktok", "TikTok"),
        ("instagram", "Instagram"),
    ]

    TONE_CHOICES = [
        ("fun", "Fun"),
        ("professional", "Professional"),
        ("motivation", "Motivation"),
        ("storytelling", "Storytelling"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="caption_generations"
    )

    topic = models.CharField(max_length=255)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    tone = models.CharField(max_length=50, choices=TONE_CHOICES)
    length = models.CharField(max_length=20, default="medium")
    cta = models.CharField(max_length=255, blank=True, null=True)

    results = models.JSONField()  # stocke les 3-5 captions

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.topic}"
