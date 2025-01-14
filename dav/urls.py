from django.urls import path, include
from . import views


urlpatterns = [

    path("administrador/", views.administrador, name="administrador"),
    path("", views.home, name="home"),
    ]