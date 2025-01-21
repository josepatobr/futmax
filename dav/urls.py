from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("administrador/", views.administrador, name="administrador"),
    path("salvar_imagem/", views.salvar_imagem, name="salvar_imagem"),
]
