from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='web_home'),
    path('login/', views.login, name='web_login'),
    path('signup/', views.signup, name='web_signup'),
]
