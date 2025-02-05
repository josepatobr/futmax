from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from decimal import Decimal
import secrets



class Produto(models.Model):
    nome = models.CharField("Nome do Produto", max_length=255, null=False, blank=False)
    detalhes = models.TextField("Detalhes", null=True, blank=True)
    preco = models.DecimalField(
        "Preço",
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        validators=[MinValueValidator(0.01), MaxValueValidator(999999.99)],
    )
    imagem = models.ImageField(
        "Imagem",
        upload_to="imagem_produto/",
        null=False,
        blank=False,
        help_text="Adicione uma imagem para o produto",
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.preco = Decimal(str(round(float(self.preco), 2)))
        super().save(*args, **kwargs)


class Promocao(models.Model):
    title = models.CharField("Título", max_length=255, null=False, blank=False)
    descricao = models.TextField("Descrição", null=True, blank=True)
    imagem = models.ImageField(
        "Imagem da Promoção", upload_to="imagem_promocao/", null=False, blank=False
    )
    produto = models.ForeignKey(
        Produto,
        verbose_name="Produto",
        on_delete=models.CASCADE,
        related_name="promocoes",
    )
    desconto = models.DecimalField(
        "Desconto",
        max_digits=5,
        decimal_places=2,
        null=False,
        blank=False,
        help_text="Desconto em porcentagem (0-100)",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    data_inicio = models.DateField("Data de Início", null=False, blank=False)
    data_fim = models.DateField("Data de Fim", null=False, blank=False)

    class Meta:
        verbose_name = "Promoção"
        verbose_name_plural = "Promoções"

    def clean(self):
        date_now = now().date()
        errors = {}

        if self.data_inicio and self.data_inicio < date_now:
            errors["data_inicio"] = "Data de início deve ser futura"

        if self.data_fim and self.data_fim < date_now:
            errors["data_fim"] = "Data de fim deve ser futura"

        if self.data_inicio and self.data_fim and self.data_inicio >= self.data_fim:
            errors["data_inicio"] = "Data de início deve ser anterior à data de fim"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_preco_com_desconto(self):
        return Decimal(
            str(round(float(self.produto.preco * (1 - self.desconto / 100)), 2))
        )

    def __str__(self):
        return f"{self.title} - {self.produto.nome} ({self.desconto}% off)"

    @property
    def is_active(self):
        current_date = now().date()
        return self.data_inicio <= current_date <= self.data_fim


class User(AbstractUser):
    email = models.EmailField("Email address", unique=True, blank=False, null=False)
    verificar_email = models.BooleanField("Email verificado", default=False)
    login_com_email = models.BooleanField("Login com email", default=False)

    def __str__(self) -> str:
        return self.username

    def get_short_name(self) -> str:
        return super().get_short_name() or self.username


class Token(models.Model):
    TIPO_EMAIL_VERIFICADO = "email_verificado"
    TIPO_LOGAR_EMAIL = "logar_email"

    TOKEN_TYPE = [
        (TIPO_EMAIL_VERIFICADO, "email_verificado"),
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
