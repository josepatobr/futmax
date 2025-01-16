from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Administrador
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

def administrador(request):
    if request.method == "POST":
        nome_completo = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpf = request.POST.get("cpf")

        try:
            admin = Administrador(
                nome_completo=nome_completo,
                email=email,
                cpf=cpf
            )
            admin.set_password(password)
            admin.save()
            
            messages.success(request, "Admin criado com sucesso.")
            return redirect("home")
        except Exception as e:
            messages.error(request, f"Erro ao criar admin: {str(e)}")
            return render(request, "dav.html")

    return render(request, "dav.html")


def home(request):
    return render(request, 'home.html')


@login_required(login_url="home")
def salvar_imagem(request: HttpRequest):
    if request.method == "POST":
        image = request.FILES.get("logo_images")
        if not image:
            messages.error(request, "Nenhuma imagem selecionada.")
            return redirect("home")

        else:
            user = request.user
            if hasattr(user, 'logo_images'):
                user.profile_image = image
                user.save()
                messages.success(request, "logo da loja atualizado.")
            else:
                messages.error



