from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest


def administrador(request:HttpRequest):
    if request.method == "POST":
        nome_completo = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpf = request.POST.get("cpf")
        foto_perfil = request.FILES.get("foto_perfil")
        try:
            user = User(
                nome_completo = nome_completo,
                email = email,
                cpf = cpf,
                foto_perfil = foto_perfil)
            user.set_password(password)
            user.save()
            
            messages.success(request, "Admin criado com sucesso.")
            return redirect("home")
        except Exception as e:
            messages.error(request, f"Erro ao criar admin: {str(e)}")
            return render(request, "dav.html")



def home(request:HttpRequest):
    if request.method == "POST":
        logo_loja = request.FILES.get("logo_loja")
        return render(request, 'home.html', {logo_loja:"logo_loja"})
    return render(request, 'home.html')

@login_required(login_url="home")
def salvar_imagem(request: HttpRequest):
    if request.method == "POST":
        image = request.FILES.get("logo_loja")
        request.user.logo_images = image
        request.user.save()
    return redirect("home")


