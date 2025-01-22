from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date



class User(AbstractUser):
    foto_perfil = models.ImageField(upload_to="foto_perfil/", null=True)
    logo_loja = models.ImageField(
        upload_to="logo_loja/",
        null=True,
        help_text="é recomendado você usar uma imagem que representa a sua loja",
    )

    def __str__(self):
        return self.username
    
class Produtos(models.Model):
    nome_produto = models.CharField(max_length=500, null=False, blank=False, editable=True)
    detalhes = models.TextField(null=False, blank=False, editable=True)
    preco = models.CharField(max_length=10, null=False, blank=False)
    data_venda = models.DateField()
    imagem_produto = models.ImageField(upload_to="imagem_produto/", null=False)

    def __str__(self):
        return self.nome_produto
    
class Produtos_promoçao(Produtos):
    imagem_promocao = models.ImageField(upload_to="imagem_promocao/", null=False)

    def __str__(self):
        return self.imagem_promocao
    
    


