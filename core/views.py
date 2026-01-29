from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import CorpoCeleste

def index(request):
    corpos = CorpoCeleste.objects.filter(categoria__in=['estrela', 'planeta'])
    return render(request, 'core/index.html', {'corpos': corpos})

def listar_corpos(request):
    todos = CorpoCeleste.objects.all()
    data = []
    for c in todos:
        item = {
            'id': c.id, 'nome': c.nome, 'categoria': c.categoria,
            'tipo': c.tipo, 'distancia': c.distancia, 'diametro': c.diametro,
            'massa': c.massa, 'temperatura': c.temperatura, 'curiosidades': c.curiosidades,
            'planeta_pai_id': c.planeta_pai.id if c.planeta_pai else None,
            'foto': c.foto.url if c.foto else None,
            'luas': []
        }
        if c.categoria == 'planeta':
            luas_vinculadas = todos.filter(planeta_pai=c)
            for lua in luas_vinculadas:
                item['luas'].append({
                    'id': lua.id, 'nome': lua.nome, 'foto': lua.foto.url if lua.foto else None
                })
        data.append(item)
    return JsonResponse(data, safe=False)

def buscar_corpos(request):
    q = request.GET.get('q', '')
    corpos = CorpoCeleste.objects.filter(nome__icontains=q)
    data = [{'id': c.id, 'nome': c.nome} for c in corpos]
    return JsonResponse(data, safe=False)

@login_required
def salvar_corpo(request, pk=None):
    if request.method == 'POST':
        corpo = get_object_or_404(CorpoCeleste, pk=pk) if pk else CorpoCeleste()
        corpo.nome = request.POST.get('nome')
        corpo.categoria = request.POST.get('categoria')
        corpo.tipo = request.POST.get('tipo', '')
        corpo.distancia = request.POST.get('distancia', '')
        corpo.diametro = request.POST.get('diametro', '')
        corpo.massa = request.POST.get('massa', '')
        corpo.temperatura = request.POST.get('temperatura', '')
        corpo.curiosidades = request.POST.get('curiosidades', '')
        pai_id = request.POST.get('planeta_pai')
        if pai_id and pai_id.isdigit():
            corpo.planeta_pai = get_object_or_404(CorpoCeleste, id=pai_id)
        else:
            corpo.planeta_pai = None
        if 'foto' in request.FILES:
            corpo.foto = request.FILES['foto']
        corpo.save()
        return JsonResponse({'status': 'sucesso'})

@login_required
def excluir_corpo(request, pk):
    if request.method == 'DELETE':
        get_object_or_404(CorpoCeleste, pk=pk).delete()
        return JsonResponse({'status': 'sucesso'})

def api_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'status': 'sucesso'})
        return JsonResponse({'status': 'erro', 'errors': form.errors}, status=400)

def api_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return JsonResponse({'status': 'sucesso'})
        return JsonResponse({'status': 'erro'}, status=400)