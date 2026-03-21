import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_captions(topic: str, platform: str, tone: str) -> list:
    prompt = f"""
    Tu es un expert en social media marketing francophone.
    
    Génère 5 légendes optimisées pour {platform}.
    
    Sujet : {topic}
    Ton : {tone}
    
    Règles :
    - Utilise des emojis adaptés
    - Ajoute un call-to-action
    - Format court et engageant
    - Marché francophone africain
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es un expert social media."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8,
    )

    content = response.choices[0].message.content

    # On découpe proprement en liste
    captions = [c.strip("- ").strip() for c in content.split("\n") if c.strip()]

    return captions[:5]
