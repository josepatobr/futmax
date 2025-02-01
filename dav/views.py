from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.contrib.auth import login
from .email import send_email

from .models import User, Token, Produto, Promocao


@login_required(login_url="cadastro")
def home(request: HttpRequest):
    produtos = Produto.objects.all()
    promocoes = Promocao.objects.all()

    # logo_loja = request.user.logo_loja.url if request.user.logo_loja else None
    return render(request, "home.html", {"produtos": produtos, "promocoes": promocoes})


def cadastro(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method != "POST":
        return render(request, "cadastro.html")

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    foto_perfil = request.FILES.get("foto_perfil")

    if User.objects.filter(email=email).exists():
        messages.error(request, "Já existe um usuário com este email.")
        return redirect("cadastro")

    if len(first_name) < 3 and len(first_name) > 20:
        messages.error(
            request, "Seu nome precisa ter no mínimo 3 letras e no máximo 20."
        )
        return redirect("cadastro")

    if len(last_name) < 3 and len(last_name) > 200:
        messages.error(
            request, "Seu sobrenome precisa ter no mínimo 3 letras e no máximo 200."
        )
        return redirect("cadastro")

    if len(password) < 4 and len(password) > 10:
        messages.error(
            request, "A senha precisa ter no mínimo 4 caracteres e no máximo 10."
        )
        return redirect("cadastro")

    try:
        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            foto_perfil=foto_perfil,
        )
        login(request, user)
        messages.success(request, "Usuário criado com sucesso.")
        return redirect("home")

    except Exception as e:
        messages.error(request, f"Erro ao criar o usuário: {str(e)}")
        return redirect("cadastro")


def login_email(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method != "POST":
        return redirect("cadastro")

    email = request.POST.get("email")

    if email is None or email.strip() == "":
        return redirect("cadastro")

    if not User.objects.filter(email=email).exists():
        return redirect("cadastro")

    if user := User.objects.filter(email=email).first():
        token = Token.objects.get_or_create(user=user, type=Token.TIPO_LOGAR_EMAIL)
        email_subject = f"Seu codigo de acesso é ({token.token})"
        email_template = "emails/codigo.html"
        send_email(user, email_subject, email_template)
        return redirect("verificacao")


def verificacao(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method != "POST":
        return render(request, "verificacao.html")

    codigo = request.POST.get("codigo")
    if token := Token.objects.filter(token=codigo).first():
        login(request, token.user)
        token.delete()
        return redirect("home")


@login_required(login_url="administrador")
def salvar_imagem(request: HttpRequest):
    if request.method == "POST":
        image = request.FILES.get("logo_loja")
        request.user.logo_loja = image
        request.user.save()
    return redirect("home")
