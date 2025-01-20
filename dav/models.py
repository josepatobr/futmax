from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
   foto_perfil = models.ImageField(upload_to='foto_perfil/', null=True)
   logo_loja = models.ImageField(upload_to='logo_loja/', null=True, help_text='é recomendado você usar uma imagem que representa a sua loja')
   
   def __str__(self):
      return self.foto_perfil
