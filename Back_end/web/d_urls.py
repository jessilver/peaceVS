from django.urls import path
from . import views
from .views import DashboardFilmesView

urlpatterns = [
    path('filmes/', DashboardFilmesView.as_view(), name='dashboard_filmes'),
]
