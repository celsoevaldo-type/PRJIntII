from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Acesso, Colaborador, Registro, Sistema


class ControleDeAcessosTeste(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user("teste", password="senha-de-teste-123")
        self.client.login(username="teste", password="senha-de-teste-123")

        self.email = Sistema.objects.create(nome="E-mail")
        self.vendas = Sistema.objects.create(nome="Vendas")
        self.maria = Colaborador.objects.create(nome="Maria", email="maria@teste.com", cargo="Vendedora",
                                                setor="Comercial", data_entrada=date(2024, 1, 10))

    def test_precisa_estar_logado(self):
        self.client.logout()
        resposta = self.client.get(reverse("colaboradores"))
        self.assertEqual(resposta.status_code, 302)  # manda para a tela de login

    def test_conceder_acesso_gera_registro(self):
        self.client.post(reverse("conceder_acesso", args=[self.maria.id]),
                         {"sistema": self.email.id, "nivel": "leitura"})
        self.assertTrue(Acesso.objects.filter(colaborador=self.maria, sistema=self.email).exists())
        self.assertTrue(Registro.objects.filter(acao__startswith="Acesso concedido", colaborador="Maria").exists())

    def test_desligar_retira_todos_os_acessos(self):
        # é o teste mais importante: quem sai não pode ficar com nenhum acesso
        Acesso.objects.create(colaborador=self.maria, sistema=self.email)
        Acesso.objects.create(colaborador=self.maria, sistema=self.vendas)

        self.client.post(reverse("desligar_colaborador", args=[self.maria.id]))
        self.maria.refresh_from_db()

        self.assertFalse(self.maria.ativo)
        self.assertEqual(self.maria.acessos.count(), 0)

    def test_nao_libera_acesso_para_desligado(self):
        self.maria.ativo = False
        self.maria.save()
        self.client.post(reverse("conceder_acesso", args=[self.maria.id]),
                         {"sistema": self.email.id, "nivel": "leitura"})
        self.assertEqual(self.maria.acessos.count(), 0)

    def test_inicio_mostra_pendencia(self):
        # desligado que ainda tem acesso (dado antigo) deve aparecer no aviso da tela inicial
        self.maria.ativo = False
        self.maria.save()
        Acesso.objects.create(colaborador=self.maria, sistema=self.email)
        resposta = self.client.get(reverse("inicio"))
        self.assertContains(resposta, "Maria")
