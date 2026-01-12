# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import CorpoCeleste

def index(request):
    # Buscamos todos os corpos para que a página já comece cheia
    corpos = CorpoCeleste.objects.all() 
    return render(request, 'core/index.html', {'corpos': corpos})

def listar_corpos(request):
    corpos = CorpoCeleste.objects.all()
    data = list(corpos.values())
    return JsonResponse(data, safe=False)

def buscar_corpos(request):
    q = request.GET.get('q', '')
    corpos = CorpoCeleste.objects.filter(nome__icontains=q)
    data = list(corpos.values())
    return JsonResponse(data, safe=False)

def filtrar_categoria(request, categoria):
    corpos = CorpoCeleste.objects.filter(categoria=categoria)
    data = list(corpos.values())
    return JsonResponse(data, safe=False)
