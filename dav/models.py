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
    foto_perfil = models.ImageField(upload_to="foto_perfil/", null=True)
    tempo_desativar = 7 # days

    ROLE_ADMIN = "admin"
    ROLE_USER = "user"

    MAX_NUM_LINKS_PER_USER = 10
    MAX_NUM_LINKS_TEMP_PER_USER = 10

    ROLE_CHOICES = [
        (ROLE_ADMIN, ("Admin")),
        (ROLE_USER, ("User")),
    ]

    role = models.CharField(("role"),
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
        help_text=("User role"))
    
    
    max_num_links = models.PositiveIntegerField(
        ("max number of links"),
        default= MAX_NUM_LINKS_PER_USER,
    )
    max_num_links_temporary = models.PositiveIntegerField(
        ("max number of temporary links"),
        default= MAX_NUM_LINKS_TEMP_PER_USER,
    )

    @property
    def is_admin(self) -> bool:
        return self.role == self.ROLE_ADMIN

    @property
    def is_user(self) -> bool:
        return self.role == self.ROLE_USER
    
    def __str__(self):
        return self.username  

    def save(self, *args, **kwargs):
        role_limits = {
            self.ROLE_ADMIN: (100, 100),
            self.ROLE_USER: (
                self.MAX_NUM_LINKS_PER_USER,
                self.MAX_NUM_LINKS_TEMP_PER_USER,
            ),
        }

        if self.is_superuser:
            self.role = self.ROLE_ADMIN
            self.email_verified = True

        if self.role in role_limits:
            self.max_num_links, self.max_num_links_temporary = role_limits[self.role]

        super().save(*args, **kwargs)


class Token(models.Model):
    DEFAULT_EXPIRY = timedelta(hours=2)

    TIPO_EMAIL_VERIFICADO = "verificar_email"
    TIPO_LOGAR_EMAIL = "logar_email"

    TOKEN_TYPE = [
        (TIPO_EMAIL_VERIFICADO,("verificar_email")),
        (TIPO_LOGAR_EMAIL,("logar_email")),
    ]

    token = models.CharField(max_length=255, unique=True, db_index=True, editable=False)
 


