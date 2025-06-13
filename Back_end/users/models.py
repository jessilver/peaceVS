from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O email deve ser definido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    # first_name e last_name já existem em AbstractUser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='profiles')
    nome_perfil = models.CharField(max_length=100)
    avatar_url = models.URLField(blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    preferencias_linguagem = models.CharField(max_length=10, default='pt-BR')
    eh_perfil_infantil = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome_perfil} ({self.user.email})"
