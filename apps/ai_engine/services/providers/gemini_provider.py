import json
import logging
from google import genai
from google.genai import types
from pydantic import BaseModel
from django.conf import settings
from .base import BaseAIProvider

logger = logging.getLogger(__name__)

class CaptionResponseSchema(BaseModel):
    captions: list[str]

class GeminiProvider(BaseAIProvider):

    def __init__(self):
        # We initialize the client once per instance
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"

    def generate_captions(self, topic: str, platform: str, tone: str, length: str = "medium", cta: str = "") -> list:
        tone_map = {
            "fun": "Fun",
            "pro": "Professionnel",
            "inspire": "Inspirant",
            "educ": "Éducatif",
            "story": "Storytelling"
        }
        human_tone = tone_map.get(tone, tone)
        
        prompt = f"""
        Génère 5 légendes créatives optimisées pour {platform}.
        Sujet : {topic}
        Ton : {human_tone}
        Longueur souhaitée : {length}
        Call-to-action spécifique (si fourni) : {cta}
        
        Règles :
        - Utilise des emojis.
        - Si un CTA est fourni, utilise-le ou adapte-le à la fin. Sinon, crée un CTA pertinent.
        - Respecte le ton demandé.
        - Pour la longueur : 
            - 'short': 1-2 phrases.
            - 'medium': un paragraphe court.
            - 'long': plusieurs paragraphes avec du storytelling.
            
        IMPORTANT : Tu dois impérativement répondre UNIQUEMENT avec un objet JSON ayant la clé "captions" qui contient un tableau de tes 5 légendes en chaîne de caractères.
        Exemple de format : {{"captions": ["Légende 1", "Légende 2"]}}
        """

        try:
            # We enforce structured JSON output by prompt & mime_type to avoid v1beta schema errors
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.7,
                )
            )
            
            # The response text should match our requested JSON: {"captions": [...]}
            data = json.loads(response.text)
            captions_list = data.get("captions", [])
            
            if isinstance(captions_list, list):
                # Clean up any potential markdown leftovers just in case
                return [c.strip() for c in captions_list[:5]]
            return []

        except Exception as e:
            logger.error(f"Erreur lors de l'appel à Gemini API: {str(e)}")
            raise e  # We raise it so the view's try/except catches it correctly or handles it
