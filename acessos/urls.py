from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("colaboradores/", views.lista_colaboradores, name="colaboradores"),
    path("colaboradores/novo/", views.novo_colaborador, name="novo_colaborador"),
    path("colaboradores/<int:id>/", views.detalhe_colaborador, name="detalhe_colaborador"),
    path("colaboradores/<int:id>/editar/", views.editar_colaborador, name="editar_colaborador"),
    path("colaboradores/<int:id>/acesso/", views.conceder_acesso, name="conceder_acesso"),
    path("colaboradores/<int:id>/desligar/", views.desligar_colaborador, name="desligar_colaborador"),
    path("acessos/<int:id>/revogar/", views.revogar_acesso, name="revogar_acesso"),
    path("sistemas/", views.lista_sistemas, name="sistemas"),
    path("sistemas/<int:id>/", views.detalhe_sistema, name="detalhe_sistema"),
    path("historico/", views.historico, name="historico"),
]
