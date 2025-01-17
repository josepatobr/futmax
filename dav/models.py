from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
   UserName = models.CharField(max_length=100, null=False, blank=True)
   foto_perfil = models.ImageField(upload_to='foto_perfil/')
   logo_loja = models.ImageField(upload_to='logo_images/', help_text="é recomendado você usar uma imagem que representa a sua loja")

def __str__(self):
    return self.UserName
