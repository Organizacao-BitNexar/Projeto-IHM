from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import CorpoCeleste
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
     # Mudamos aqui para excluir a categoria 'lua' da página inicial
    corpos = CorpoCeleste.objects.exclude(categoria='moon')
    return render(request, 'core/index.html', {'corpos': corpos})

def listar_corpos(request):
    corpos = CorpoCeleste.objects.all()
    data = []
    for c in corpos:
        data.append({
            'id': c.id,
            'nome': c.nome,
            'categoria': c.categoria,
            'tipo': c.tipo,
            'distancia': c.distancia,
            'curiosidades': c.curiosidades,
            'foto': c.foto.url if c.foto else None,
            'planeta_pai_id': c.planeta_pai_id,
        })
    return JsonResponse(data, safe=False)

# ESTA É A FUNÇÃO QUE ESTAVA FALTANDO/DANDO ERRO
def buscar_corpos(request):
    q = request.GET.get('q', '')
    corpos = CorpoCeleste.objects.filter(nome__icontains=q)
    data = list(corpos.values())
    return JsonResponse(data, safe=False)

def filtrar_categoria(request, categoria):
    corpos = CorpoCeleste.objects.filter(categoria=categoria)
    data = list(corpos.values())
    return JsonResponse(data, safe=False)

@csrf_exempt
def salvar_corpo(request, pk=None):
    if request.method == 'POST':
        if pk:
            corpo = get_object_or_404(CorpoCeleste, pk=pk)
        else:
            corpo = CorpoCeleste()

        corpo.nome = request.POST.get('nome')
        corpo.categoria = request.POST.get('categoria')
        corpo.tipo = request.POST.get('tipo', '')
        corpo.distancia = request.POST.get('distancia', '')
        corpo.curiosidades = request.POST.get('curiosidades', '')

        pai_id = request.POST.get('planeta_pai')
        if pai_id and corpo.categoria == 'moon':
            corpo.planeta_pai_id = pai_id
        else:
            corpo.planeta_pai = None # Se não for lua, garante que não tem pai

        if 'foto' in request.FILES:
            corpo.foto = request.FILES['foto']
        
        corpo.save()
        return JsonResponse({'status': 'sucesso'})

def excluir_corpo(request, pk):
    if request.method == 'DELETE':
        corpo = get_object_or_404(CorpoCeleste, pk=pk)
        corpo.delete()
        return JsonResponse({'status': 'sucesso'})