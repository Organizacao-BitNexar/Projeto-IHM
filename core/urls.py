from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/corpos/', views.api_corpos, name='api_corpos'),
    path('api/buscar/', views.buscar_corpos, name='buscar_corpos'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/signup/', views.api_signup, name='api_signup'),
    path('api/salvar/', views.salvar_corpo, name='salvar_novo'),
    path('api/salvar/<int:pk>/', views.salvar_corpo, name='editar_corpo'),
    path('api/excluir/<int:pk>/', views.excluir_corpo, name='excluir_corpo'),
]