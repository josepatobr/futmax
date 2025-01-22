from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Produtos, Produtos_promoçao
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib.auth import login



def administrador(request: HttpRequest):
    if request.method != "POST":
        return render(request, "dav.html")

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    foto_perfil = request.FILES.get("foto_perfil")

    if User.objects.filter(email=email).exists():
        messages.error(request, "Já existe um administrador com este email.")
        return redirect("dav")
    
    if len(first_name) < 3 and len(first_name) > 20:
        messages.error(request, "Seu nome precisa ter no mínimo 3 letras e no máximo 20.")
        return render(request, "dav.html")

    if len(last_name) < 3 and len(last_name) > 200:
        messages.error(request, "Seu sobrenome precisa ter no mínimo 3 letras e no máximo 200.")
        return render(request, "dav.html")

    if len(password) < 4 and len(password) > 10:
        messages.error(request, "A senha precisa ter no mínimo 4 caracteres e no máximo 10.")
        return render(request, "dav.html")

    
    try:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            foto_perfil=foto_perfil,
        )
        login(request, user)
        messages.success(request, "Admin criado com sucesso.")
        return redirect("home")

    except Exception as e:
        messages.error(request, f"Erro ao criar o admin: {str(e)}")
        return redirect("dav")

      
def home(request:HttpRequest):
    if request.user.is_authenticated:
        return render(request, "home.html")
    
    if request.method == "POST":
        imagem_produto = Produtos.objects.all()
        imagem_promocao = Produtos_promoçao.objects.all()
        logo_loja = request.FILES.get("logo_loja")
        return render(request, 'home.html', {logo_loja:"logo_loja"}, 
                      {imagem_produto:"imagem_produto"}, 
                      {imagem_promocao:"imagem_promocao"})
    

@login_required(login_url="home")
def salvar_imagem(request: HttpRequest):
    if request.method == "POST":
        image = request.FILES.get("logo_loja")
        request.user.logo_loja = image
        request.user.save()
    return redirect("home")


