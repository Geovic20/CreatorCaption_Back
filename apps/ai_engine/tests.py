from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch
from apps.ai_engine.models import CaptionGeneration
from apps.billing.models import Subscription

User = get_user_model()

class QuotaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_free = User.objects.create_user(email="free@test.com", password="password", first_name="Free", last_name="User")
        Subscription.objects.create(user=self.user_free, plan="free")

        self.user_pro = User.objects.create_user(email="pro@test.com", password="password", first_name="Pro", last_name="User")
        Subscription.objects.create(user=self.user_pro, plan="pro")

        self.user_no_sub = User.objects.create_user(email="nosub@test.com", password="password", first_name="No", last_name="Sub")
        # Ensure the user has no subscription explicitly created
        
        self.generate_url = reverse('generate_captions') # Note: Assuming this URL exists and maps to generate_captions_view
        
    def _create_generations(self, user, count):
        for _ in range(count):
            CaptionGeneration.objects.create(
                user=user,
                topic="Test Sub",
                platform="tiktok",
                tone="fun",
                length="short",
                cta="Follow",
                results={"captions": ["Caption 1"]}
            )

    @patch('apps.ai_engine.services.ai_router.AIRouter.get_provider')
    def test_free_user_under_quota_can_generate(self, mock_get_provider):
        mock_provider = mock_get_provider.return_value
        mock_provider.generate_captions.return_value = ["Test Caption"]
        
        self.client.force_authenticate(user=self.user_free)
        self._create_generations(self.user_free, 9)
        
        response = self.client.post("/api/ai_engine/generate/", { # Using hardcoded url instead of reverse to be safe since I don't know the urls configuration
            "topic": "Test",
            "platform": "tiktok",
            "tone": "fun"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('apps.ai_engine.services.ai_router.AIRouter.get_provider')
    def test_free_user_over_quota_blocked(self, mock_get_provider):
        self.client.force_authenticate(user=self.user_free)
        self._create_generations(self.user_free, 10)
        
        response = self.client.post("/api/ai_engine/generate/", {
            "topic": "Test",
            "platform": "tiktok",
            "tone": "fun"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["code"], "QUOTA_EXCEEDED")

    @patch('apps.ai_engine.services.ai_router.AIRouter.get_provider')
    def test_pro_user_over_quota_can_generate(self, mock_get_provider):
        mock_provider = mock_get_provider.return_value
        mock_provider.generate_captions.return_value = ["Test Caption"]

        self.client.force_authenticate(user=self.user_pro)
        self._create_generations(self.user_pro, 15)
        
        response = self.client.post("/api/ai_engine/generate/", {
            "topic": "Test",
            "platform": "tiktok",
            "tone": "fun"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('apps.ai_engine.services.ai_router.AIRouter.get_provider')
    def test_no_subscription_defaults_to_free(self, mock_get_provider):
        self.client.force_authenticate(user=self.user_no_sub)
        self._create_generations(self.user_no_sub, 10)
        
        response = self.client.post("/api/ai_engine/generate/", {
            "topic": "Test",
            "platform": "tiktok",
            "tone": "fun"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["code"], "QUOTA_EXCEEDED")
