from django.db import models

class Administrador(models.Model):
    nome_completo = models.CharField(max_length=30)
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length=20)    
    cpf = models.CharField(max_length=14, primary_key=True, null=False)
    logo_images = models.ImageField(upload_to='logo_images/', blank=True, null=True)

    def __str__(self):
        return self.nome_completo
