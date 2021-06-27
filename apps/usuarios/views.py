from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages

from receitas.models import Receita


def cadastro(request):
    """Cadastra uma nova pessoa no sistema"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if checa_campos_vazios(request, [('nome', nome), ('email', email), ]):
            return redirect('cadastro')
        if password != password2:
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário com esse email já existe')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário com esse nome já existe')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=password)
        messages.success(request, 'Usuário cadastrado com sucesso')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html') 

def login(request):
    """Realiza login de uma pessoa no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if email == "" or senha == "":
            messages.error(request, "Campos email e senha não podem ficar em branco")
            return redirect('login')
        if User.objects.filter(email=email).exists():
            username = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=username, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        id_user = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(
            pessoa=id_user
        )
        dados = {
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def checa_campos_vazios(request, campos: list(tuple())):
    """Verifica campos vazios e cria mensagens de alerta"""
    erro = False
    for nome, valor in campos:
        if not valor.strip():
            messages.error(request, f'O campo {nome} não pode ficar em branco')
            erro = True
    return erro