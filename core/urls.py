from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/corpos/', views.listar_corpos),
    path('api/buscar/', views.buscar_corpos),
    path('api/categoria/<str:categoria>/', views.filtrar_categoria),
]
