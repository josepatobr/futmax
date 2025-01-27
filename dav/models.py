from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets


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
    email = models.EmailField("Email address", unique=True, blank=False, null=False)
    verificar_email = models.BooleanField("Email verificado", default=False)
    login_com_email = models.BooleanField("Login com email", default=False)
    foto_perfil = models.ImageField(upload_to="foto_perfil/", null=True)

    def __str__(self) -> str:
        return self.username

    def get_short_name(self) -> str:
        return super().get_short_name() or self.username


class Token(models.Model):
    TIPO_EMAIL_VERIFICADO = "verificar_email"
    TIPO_LOGAR_EMAIL = "logar_email"

    TOKEN_TYPE = [
        (TIPO_EMAIL_VERIFICADO, "verificar_email"),
        (TIPO_LOGAR_EMAIL, "logar_email"),
    ]

    type = models.CharField(
        max_length=20,
        choices=TOKEN_TYPE,
        default=TIPO_EMAIL_VERIFICADO,
        help_text="Type of token",
    )
    token = models.CharField(max_length=255, unique=True, db_index=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.type}"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super().save(*args, **kwargs)

    def generate_token(self, length: int = 4):
        return secrets.token_bytes(length).hex()
