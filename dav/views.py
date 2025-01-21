from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
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

@login_required(login_url="home")
def salvar_imagem(request: HttpRequest):
    if request.method == "POST":
        image = request.FILES.get("logo_loja")
        request.user.logo_loja = image
        request.user.save()
    return redirect("home")
      
def home(request:HttpRequest):
    if request.method == "POST":
        logo_loja = request.FILES.get("logo_loja")
        return render(request, 'home.html', {logo_loja:"logo_loja"})
    return render(request, 'home.html')


