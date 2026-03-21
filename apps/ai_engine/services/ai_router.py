from django.conf import settings
from .providers.openai_provider import OpenAIProvider
from .providers.gemini_provider import GeminiProvider

class AIRouter:

    PROVIDERS = {
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
    }

    @classmethod
    def get_provider(cls):
        provider_name = getattr(settings, "AI_PROVIDER", "gemini")
        provider_class = cls.PROVIDERS.get(provider_name)

        if not provider_class:
            raise ValueError("Provider IA invalide")

        return provider_class()

        