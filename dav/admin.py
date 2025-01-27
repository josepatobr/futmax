from .models import User, Produto, ProdutoPromocao, Token
from django.contrib import admin

admin.site.register(User)
admin.site.register(Token)
admin.site.register(Produto)
admin.site.register(ProdutoPromocao)
