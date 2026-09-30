from django.contrib.auth.models import User
from django.db import models


class Colaborador(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=80)
    setor = models.CharField(max_length=80)
    data_entrada = models.DateField()
    ativo = models.BooleanField(default=True)  # False = desligado da empresa

    class Meta:
        ordering = ["nome"]
        verbose_name_plural = "colaboradores"

    def __str__(self):
        return self.nome


class Sistema(models.Model):
    # sistemas e informações da empresa: e-mail, ERP, pasta do financeiro, etc.
    nome = models.CharField(max_length=80, unique=True)
    descricao = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Acesso(models.Model):
    NIVEIS = [
        ("leitura", "Só leitura"),
        ("edicao", "Leitura e edição"),
        ("admin", "Administrador"),
    ]

    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name="acessos")
    sistema = models.ForeignKey(Sistema, on_delete=models.CASCADE, related_name="acessos")
    nivel = models.CharField(max_length=10, choices=NIVEIS, default="leitura")
    concedido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        # a mesma pessoa não pode ter dois acessos ao mesmo sistema
        unique_together = ["colaborador", "sistema"]

    def __str__(self):
        return f"{self.colaborador} - {self.sistema}"


class Registro(models.Model):
    # histórico de tudo que foi feito: quem mexeu, quando e em quem.
    # guardamos o nome em texto porque o colaborador ou o sistema podem ser apagados depois
    feito_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)
    acao = models.CharField(max_length=40)
    colaborador = models.CharField(max_length=120)
    sistema = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["-data"]

    def __str__(self):
        return f"{self.data:%d/%m/%Y %H:%M} - {self.acao} - {self.colaborador}"
