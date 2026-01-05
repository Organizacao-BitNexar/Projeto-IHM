from django.contrib import admin
from django.urls import path, include
from core import views  # Importa o módulo views inteiro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), # Usa views.home
    path('', include('core.urls')),
]