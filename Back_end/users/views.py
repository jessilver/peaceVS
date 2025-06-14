from django.shortcuts import render
from rest_framework import viewsets
from .models import CustomUser, UserProfile
from .serializers import CustomUserSerializer, CustomUserSignupSerializer, UserProfileSerializer, CustomAuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions

# Create your views here.

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Só permite que o usuário veja/edite seus próprios perfis
        user = self.request.user
        if user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
        }, status=status.HTTP_200_OK)

class UserSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSignupSerializer
    permission_classes = [AllowAny]
