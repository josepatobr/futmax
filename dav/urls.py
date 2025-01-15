from django.urls import path, include
from . import views


urlpatterns = [

    path("administrador/", views.administrador, name="administrador"),
    path("", views.home, name="home"),
    path("salvar_imagem/", views.salvar_imagem, name="salvar_imagem"),

]