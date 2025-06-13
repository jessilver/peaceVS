from django.contrib import admin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('-date_joined',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('nome_perfil', 'user', 'eh_perfil_infantil', 'preferencias_linguagem')
    search_fields = ('nome_perfil', 'user__email')
    list_filter = ('eh_perfil_infantil', 'preferencias_linguagem')
