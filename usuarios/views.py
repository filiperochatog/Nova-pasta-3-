from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Usuario
from hashlib import sha256

def login(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    resposta = f"{nome} {email} {senha}"
    
    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')

    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')
    
    senha_hash = sha256(senha.encode()).hexdigest()

    if Usuario.objects.filter(email=email).exists():
        return redirect('/auth/cadastro/?status=3')

    try:
        usuario = Usuario(nome=nome,
                          email=email,
                          senha=senha_hash
                          )
        usuario.save()
        return redirect('/auth/cadastro/?status=0')
    except Exception as e:
        print(e)
        return redirect('/auth/cadastro/?status=4')
    
def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    # Calcula o hash da senha fornecida
    senha_hash = sha256(senha.encode()).hexdigest()

    # Verifica se existe um usuário com o email fornecido
    usuario = Usuario.objects.filter(email=email).first()

    if usuario is None:
        # Se não houver nenhum usuário com esse email, redireciona com status=1
        return redirect('/auth/login/?status=1')
    else:
        # Verifica se a senha fornecida coincide com a senha armazenada
        if usuario.senha == senha_hash:
            # Senha correta, define a variável de sessão 'logado' como True
            request.session['logado'] = True
            # Redireciona para a página inicial da plataforma
            return redirect('/plataforma/home')
        else:
            # Senha incorreta, redireciona com status=1
            return redirect('/auth/login/?status=1')

def sair(request):
    # Limpa a variável de sessão 'logado'
    request.session.flush()
    # Redireciona para a página de login
    return redirect('/auth/login/')
