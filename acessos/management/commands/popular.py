from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from acessos.models import Acesso, Colaborador, Registro, Sistema

# dados inventados, só para mostrar o sistema funcionando.
# nomes e e-mails são fictícios
SISTEMAS = [
    ("E-mail corporativo", "Contas de e-mail da empresa"),
    ("Sistema de vendas", "Pedidos, clientes e orçamentos"),
    ("Pasta do financeiro", "Planilhas de contas a pagar e receber"),
    ("Estoque", "Controle de entrada e saída de produtos"),
    ("Redes sociais", "Perfis da empresa no Instagram e Facebook"),
]

COLABORADORES = [
    ("Ana Paula Souza", "ana@empresa.exemplo", "Gerente", "Administrativo", date(2019, 3, 11), True,
     [("E-mail corporativo", "admin"), ("Pasta do financeiro", "edicao"), ("Sistema de vendas", "leitura")]),
    ("Bruno Lima", "bruno@empresa.exemplo", "Vendedor", "Comercial", date(2022, 7, 4), True,
     [("E-mail corporativo", "edicao"), ("Sistema de vendas", "edicao")]),
    ("Carla Mendes", "carla@empresa.exemplo", "Assistente financeira", "Financeiro", date(2021, 1, 18), True,
     [("E-mail corporativo", "edicao"), ("Pasta do financeiro", "edicao")]),
    ("Diego Rocha", "diego@empresa.exemplo", "Estoquista", "Logística", date(2023, 5, 2), True,
     [("E-mail corporativo", "edicao"), ("Estoque", "edicao")]),
    ("Elaine Castro", "elaine@empresa.exemplo", "Social media", "Marketing", date(2024, 2, 19), True,
     [("E-mail corporativo", "edicao"), ("Redes sociais", "admin")]),
    # este caso imita o problema da visita: saiu da empresa e continuou com acesso
    ("Fábio Nunes", "fabio@empresa.exemplo", "Vendedor", "Comercial", date(2020, 9, 14), False,
     [("E-mail corporativo", "edicao"), ("Sistema de vendas", "edicao")]),
]


class Command(BaseCommand):
    help = "Cria um usuário de teste e alguns dados de exemplo"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "", "admin123")

        for nome, descricao in SISTEMAS:
            Sistema.objects.get_or_create(nome=nome, defaults={"descricao": descricao})

        for nome, email, cargo, setor, entrada, ativo, acessos in COLABORADORES:
            colaborador, criado = Colaborador.objects.get_or_create(
                email=email,
                defaults={"nome": nome, "cargo": cargo, "setor": setor,
                          "data_entrada": entrada, "ativo": ativo},
            )
            if not criado:
                continue
            Registro.objects.create(acao="Cadastro", colaborador=nome)
            for nome_sistema, nivel in acessos:
                sistema = Sistema.objects.get(nome=nome_sistema)
                Acesso.objects.create(colaborador=colaborador, sistema=sistema, nivel=nivel)
                Registro.objects.create(acao="Acesso concedido", colaborador=nome, sistema=nome_sistema)

        self.stdout.write("Pronto. Entre com usuário admin e senha admin123.")
