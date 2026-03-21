import os
from openai import OpenAI
from django.conf import settings
from .base import BaseAIProvider

class OpenAIProvider(BaseAIProvider):

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_captions(self, topic: str, platform: str, tone: str) -> list:

        prompt = f"""
        Génère 5 légendes optimisées pour {platform}.
        Sujet : {topic}
        Ton : {tone}
        Utilise des emojis et un call-to-action.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un expert social media."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
        )

        content = response.choices[0].message.content
        captions = [c.strip("- ").strip() for c in content.split("\n") if c.strip()]

        return captions[:5]                                                               