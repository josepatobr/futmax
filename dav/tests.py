from django.test import TestCase
from dav.models import Token

import string
import secrets
itens = (string.ascii_letters + string.ascii_lowercase)
senha = [secrets.choice(itens) for i in range (20)]
senha = "".join(senha)

print(senha)