from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    foto_perfil = models.ImageField(upload_to="foto_perfil/", null=True)
    logo_loja = models.ImageField(
        upload_to="logo_loja/",
        null=True,
        help_text="é recomendado você usar uma imagem que representa a sua loja",
    )

    def __str__(self):
        return self.username


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
