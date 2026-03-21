import os
import sys
import django

sys.path.append(r"C:\Users\kposs\Documents\Mes projets\CreatorCaption\Code source\Backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.conf import settings
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)
for m in client.models.list(config={'page_size': 50}):
    print(m.name, m.supported_actions)
