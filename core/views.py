from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from .models import CorpoCeleste

# Função auxiliar para verificar se é superusuário
def admin_only(user):
    return user.is_superuser

def index(request):
    # Mostra apenas Estrelas e Planetas (que não têm pai) na grade principal
    corpos = CorpoCeleste.objects.filter(planeta_pai__isnull=True)
    return render(request, 'core/index.html', {'corpos': corpos})

def api_corpos(request):
    todos = CorpoCeleste.objects.all()
    data = []
    for c in todos:
        item = {
            'id': c.id,
            'nome': c.nome,
            'categoria': c.categoria,
            'tipo': c.tipo,
            'distancia': c.distancia,
            'diametro': c.diametro,
            'massa': c.massa,
            'temperatura': c.temperatura,
            'curiosidades': c.curiosidades,
            'planeta_pai_id': c.planeta_pai.id if c.planeta_pai else None,
            'foto': c.foto.url if c.foto else None,
            'luas': []
        }
        if c.categoria == 'planeta':
            luas_vinculadas = todos.filter(planeta_pai=c)
            for lua in luas_vinculadas:
                item['luas'].append({
                    'id': lua.id,
                    'nome': lua.nome,
                    'foto': lua.foto.url if lua.foto else None
                })
        data.append(item)
    return JsonResponse(data, safe=False)

def buscar_corpos(request):
    q = request.GET.get('q', '')
    corpos = CorpoCeleste.objects.filter(nome__icontains=q)
    data = [{'id': c.id, 'nome': c.nome} for c in corpos]
    return JsonResponse(data, safe=False)

def api_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'status': 'sucesso'})
    return JsonResponse({'status': 'erro'}, status=400)

def api_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'status': 'sucesso'})
        return JsonResponse({'status': 'erro', 'errors': form.errors.as_json()}, status=400)
    return JsonResponse({'status': 'erro'}, status=400)

@user_passes_test(admin_only)
def salvar_corpo(request, pk=None):
    if request.method == 'POST':
        corpo = get_object_or_404(CorpoCeleste, pk=pk) if pk else CorpoCeleste()
        
        # Pega o novo valor, mas se vier vazio, mantém o que já estava no banco (corpo.campo)
        corpo.nome = request.POST.get('nome', corpo.nome)
        corpo.categoria = request.POST.get('categoria', corpo.categoria)
        corpo.tipo = request.POST.get('tipo', corpo.tipo)
        corpo.distancia = request.POST.get('distancia', corpo.distancia)
        corpo.massa = request.POST.get('massa', corpo.massa)
        corpo.temperatura = request.POST.get('temperatura', corpo.temperatura)
        corpo.curiosidades = request.POST.get('curiosidades', corpo.curiosidades)

        pai_id = request.POST.get('planeta_pai')
        if pai_id and pai_id.isdigit():
            corpo.planeta_pai = get_object_or_404(CorpoCeleste, id=pai_id)
        # Se for novo ou se mudou a categoria no formulário:
        elif request.POST.get('categoria') != 'lua':
            corpo.planeta_pai = None

        if 'foto' in request.FILES:
            corpo.foto = request.FILES['foto']
        
        corpo.save()
        return JsonResponse({'status': 'sucesso'})
@user_passes_test(admin_only)
def excluir_corpo(request, pk):
    if request.method == 'DELETE':
        corpo = get_object_or_404(CorpoCeleste, pk=pk)
        corpo.delete()
        return JsonResponse({'status': 'sucesso'})