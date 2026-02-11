from rest_framework.views import APIView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, ChangePasswordSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

# Vues pour l'inscription
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)

# Vue pour la connexion
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

# Vue pour récupérer les données de l'utilisateur
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# Vue pour le changement de mot de passe
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response(
                {"detail": "Mot de passe modifié avec succès"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue pour la demande de réinitialisation de mot de passe
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user =  User.objects.get(email=serializer.validated_data["email"])

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"

        send_mail(
            subject="Réinitialisation de votre mot de passe",
            message=f"Cliquez sur ce lien pour réinitialiser votre mot de passe : {reset_link}",
            from_email="[EMAIL_ADDRESS]",
            recipient_list=[user.email],
        )

        return Response({
            "detail": "Lien de réinitialisation envoyé"
        }, status=status.HTTP_200_OK)

# Vue pour la confirmation du nouveau mot de passe
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data["uid"]))
            user = User.objects.get(pk=uid)
        except Exception as e:
            return Response({"detail": "Lien invalide"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not token_generator.check_token(user, serializer.validated_data["token"]):
            return Response({"detail": "Lien invalide ou expiré"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        
        return Response({"detail": "Mot de passe modifié avec succès"}, status=status.HTTP_200_OK)

# Fonctions utilitaires pour l'envoi d'emails
def build_reset_password_link(request, uid, token):
    frontend_url = settings.FRONTEND_URL  # ex: https://creatorcaption.com
    return f"{frontend_url}/reset-password/{uid}/{token}"

# Fonction pour envoyer l'email de réinitialisation de mot de passe    
def send_reset_password_email(user, uid, token):
    reset_link = build_reset_link(None, uid, token)

    subject = "Réinitialisation de votre mot de passe – CreatorCaption"
    from_email = "CreatorCaption <no-reply@creatorcaption.com>"
    to = [user.email]

    html_content = render_to_string(
        "emails/reset_password.html",
        {"reset_link": reset_link}
    )

    text_content = f"""
    Réinitialisation de mot de passe

    Utilisez ce lien pour définir un nouveau mot de passe :
    {reset_link}

    Ce lien est valable 24 heures.
    """

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()