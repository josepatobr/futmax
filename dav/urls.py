from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login_email/", views.login_email, name="login_email"),
    path("verificacao/", views.verificacao, name="verificacao"),
    path("salvar_imagem/", views.salvar_imagem, name="salvar_imagem"),
]
