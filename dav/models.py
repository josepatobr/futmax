from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta

class Produto(models.Model):
    nome = models.CharField(max_length=500, null=False, blank=False)
    detalhes = models.TextField(null=False, blank=False)
    preco = models.CharField(max_length=10, null=False, blank=False)
    data_venda = models.DateField()
    imagem = models.ImageField(upload_to="imagem_produtos/", null=False)

    def __str__(self):
        return self.nome


class ProdutoPromocao(Produto):
    promocao_imagem = models.ImageField(upload_to="imagem_promocoes/", null=False)

    def __str__(self):
        return self.nome
    

class User(AbstractUser):

    email = models.EmailField(("email address"), unique=True, blank=False, null=False)
    verificar_email = models.BooleanField(("email verificado"), default=False)
    login_com_email = models.BooleanField(("login com email"), default=False)
    foto_perfil = models.ImageField(upload_to="foto_perfil/", null=True, blank=False)
    tempo_desativar = 7 # days
    
    def __str__(self):
        return self.username  


class Token(models.Model):
    DEFAULT_EXPIRY = timedelta(hours=2)

    TIPO_EMAIL_VERIFICADO = "verificar_email"
    TIPO_LOGAR_EMAIL = "logar_email"

    TOKEN_TYPE = [
        (TIPO_EMAIL_VERIFICADO,("verificado_email")),
        (TIPO_LOGAR_EMAIL,("logar_email")),
    ]

    token = models.CharField(max_length=8, unique=True, db_index=True, editable=False)
 

