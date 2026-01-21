from django.urls import path
from . import views

urlpatterns = [
    path('api/corpos/', views.listar_corpos, name='listar_corpos'),
    path('api/buscar/', views.buscar_corpos, name='buscar_corpos'),
    path('api/categoria/<str:categoria>/', views.filtrar_categoria, name='filtrar_categoria'),
    path('api/salvar/', views.salvar_corpo, name='salvar_novo'), # POST
    path('api/salvar/<int:pk>/', views.salvar_corpo, name='editar_corpo'), # PUT/POST
    path('api/excluir/<int:pk>/', views.excluir_corpo, name='excluir_corpo'), # DELETE
]