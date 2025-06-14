from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, UserProfile

class CustomUserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    nome_perfil = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'nome_perfil']

    def create(self, validated_data):
        password = validated_data.pop('password')
        nome_perfil = validated_data.pop('nome_perfil', None)
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        # Cria perfil padrão automaticamente
        UserProfile.objects.create(
            user=user,
            nome_perfil=nome_perfil or f"Perfil de {user.first_name or user.email}",
            eh_perfil_infantil=False
        )
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'nome_perfil', 'avatar_url', 'data_nascimento', 'preferencias_linguagem', 'eh_perfil_infantil']

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
        else:
            raise serializers.ValidationError('Must include "email" and "password".', code='authorization')
        attrs['user'] = user
        return attrs
