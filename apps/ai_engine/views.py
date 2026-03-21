from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CaptionGeneration
from .serializers import CaptionGenerationSerializer
from .services.ai_router import AIRouter

# Génération de légendes
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_captions_view(request):
    serializer = CaptionGenerationSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Appel IA
    try:
        provider = AIRouter.get_provider()
        captions = provider.generate_captions(
            topic=serializer.validated_data["topic"],
            platform=serializer.validated_data["platform"],
            tone=serializer.validated_data["tone"],
            length=serializer.validated_data.get("length") or "medium",
            cta=serializer.validated_data.get("cta") or "",
        )

        # Sauvegarde en attente
        db_entry = CaptionGeneration.objects.create(
            user=request.user,
            topic=serializer.validated_data["topic"],
            platform=serializer.validated_data["platform"],
            tone=serializer.validated_data["tone"],
            length=serializer.validated_data.get("length") or "medium",
            cta=serializer.validated_data.get("cta") or "",
            results={"captions": captions},
        )

        return Response(
            {
                "id": db_entry.id,
                "captions": captions,
                "created_at": db_entry.created_at,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {"error": f"Erreur lors de la génération: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# Historique des légendes
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def history_view(request):
    generations = CaptionGeneration.objects.filter(user=request.user)
    serializer = CaptionGenerationSerializer(generations, many=True)
    return Response(serializer.data)
