from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
import secrets



ROLE_DESCONTO_5 = 5
ROLE_DESCONTO_10 = 10
ROLE_DESCONTO_15 = 15
ROLE_DESCONTO_20 = 20
ROLE_DESCONTO_25 = 25

ROLE_CHOICES = [
    (5, "5%"),
    (10, "10%"),
    (15, "15%"),
    (20, "20%"),
    (25, "25%"),
]



class Produto(models.Model):
    nome = models.CharField(max_length=500, null=False, blank=False)
    detalhes = models.TextField(null=True, blank=False)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    data_venda = models.DateField()
    imagem = models.ImageField(upload_to="imagem_produto/", null=False, blank=False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.preco is not None:
            self.preco = round(self.preco, 2)
        

class ProdutoPromocao(models.Model):
    nome = models.CharField(max_length=500, null=False, blank=False)
    especificacoes  = models.TextField(null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    imagem_promocao = models.ImageField(upload_to="imagem_promocao/", null=False, blank=False)
    limite_maximo = models.DateField(help_text="defina até quando pode ser escolhida uma data de expiração", null=False, blank=False)
    expiracao_data = models.DateField(help_text="escolha uma data dentro do limite definido", null=False, blank=False)
    desconto = models.IntegerField(choices=ROLE_CHOICES, default=10)



    def clean(self):
        if self.expiracao_data > self.limite_maximo:
            raise ValidationError({"expiracao_data": "a data de expiração não pode ser maior que o limite maximo escolhido"})
        if self.expiracao_data < now().date():
            raise ValidationError({"expiracao_data": "a data de expiração não pode estar no passado"})

    def aplicar_desconto(self, preco):
        valor_desconto = (preco * self.desconto) / 100
        preco_final = preco - valor_desconto
        return preco_final
        
    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.preco is not None:
            self.preco = round(self.preco, 2)
        super().save(*args, **kwargs)

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
