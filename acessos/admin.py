from django.contrib import admin

from .models import Acesso, Colaborador, Registro, Sistema

admin.site.register(Colaborador)
admin.site.register(Sistema)
admin.site.register(Acesso)
admin.site.register(Registro)
