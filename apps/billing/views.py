from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Subscription

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mock_upgrade_view(request):
    """
    Vue de simulation pour passer au plan Pro.
    En production, cela serait géré par un webhook Stripe ou Fedapay.
    """
    subscription, created = Subscription.objects.get_or_create(user=request.user)
    subscription.plan = 'pro'
    subscription.save()
    
    return Response({
        "message": "Félicitations ! Vous êtes maintenant membre Pro.",
        "plan": subscription.plan
    }, status=status.HTTP_200_OK)
