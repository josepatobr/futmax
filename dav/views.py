from django.shortcuts import render, redirect
from .models import Administrador
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout


from django.shortcuts import render
from django.contrib import messages
from .models import Administrador

def administrador(request):
    if request.method == "POST":
        nome_completo = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpf = request.POST.get("cpf")

        try:
            user = Administrador.objects.create_user(
                nome_completo=nome_completo, email=email, password=password, cpf=cpf
            )
            messages.success(request, "Admin criado com sucesso")
            return render(request, "home.html") 
        except Exception as e:
            messages.error(request, f"Erro ao criar admin: {str(e)}")
            return render(request, "dav.html")

    return render(request, "dav.html") 

def home(request):
    return render(request, "home.html")



