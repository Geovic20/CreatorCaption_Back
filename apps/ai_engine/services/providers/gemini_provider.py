import json
import logging
from google import genai
from google.genai import types
from django.conf import settings
from .base import BaseAIProvider

logger = logging.getLogger(__name__)

class GeminiProvider(BaseAIProvider):

    def __init__(self):
        # We initialize the client once per instance
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-1.5-flash"

    def generate_captions(self, topic: str, platform: str, tone: str) -> list:
        prompt = f"""
        Génère 5 légendes créatives optimisées pour {platform}.
        Sujet : {topic}
        Ton : {tone}
        Utilise des emojis et un call-to-action à la fin de chaque légende.
        """

        try:
            # We enforce structured JSON output to guarantee a list of strings is returned
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema={
                        "type": "ARRAY",
                        "items": {
                            "type": "STRING",
                            "description": "Une légende générée pour le réseau social"
                        }
                    },
                    temperature=0.7,
                )
            )
            
            # The response text should be a valid JSON array of strings
            captions = json.loads(response.text)
            
            if isinstance(captions, list):
                # Clean up any potential markdown leftovers just in case
                return [c.strip() for c in captions[:5]]
            return []

        except Exception as e:
            logger.error(f"Erreur lors de l'appel à Gemini API: {str(e)}")
            return ["Désolé, une erreur technique est survenue lors de la génération (Gemini)."]