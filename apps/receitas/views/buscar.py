from django.shortcuts import render

from receitas.models import Receita


def buscar(request):
    lista_receitas = Receita.objects.filter(publicada=True).order_by('-date_receita')
    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)
    dados = {
        'receitas': lista_receitas
    }
    return render(request, 'receitas/buscar.html', dados)