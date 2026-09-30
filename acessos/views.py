from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import AcessoForm, ColaboradorForm, SistemaForm
from .models import Acesso, Colaborador, Registro, Sistema


def registrar(request, acao, colaborador, sistema=""):
    Registro.objects.create(feito_por=request.user, acao=acao,
                            colaborador=str(colaborador), sistema=str(sistema))


@login_required
def inicio(request):
    # pessoas que já saíram da empresa mas ainda aparecem com algum acesso.
    # é exatamente o problema que ouvimos na visita, então fica em destaque na tela
    pendencias = Colaborador.objects.filter(ativo=False, acessos__isnull=False).distinct()

    contexto = {
        "total_ativos": Colaborador.objects.filter(ativo=True).count(),
        "total_sistemas": Sistema.objects.count(),
        "total_acessos": Acesso.objects.count(),
        "pendencias": pendencias,
        "ultimos_registros": Registro.objects.all()[:5],
    }
    return render(request, "acessos/inicio.html", contexto)


@login_required
def lista_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, "acessos/colaboradores.html", {"colaboradores": colaboradores})


@login_required
def novo_colaborador(request):
    form = ColaboradorForm(request.POST or None)
    if form.is_valid():
        colaborador = form.save()
        registrar(request, "Cadastro", colaborador)
        messages.success(request, f"{colaborador} cadastrado(a).")
        return redirect("detalhe_colaborador", colaborador.id)
    return render(request, "acessos/form.html", {"form": form, "titulo": "Novo colaborador"})


@login_required
def editar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    form = ColaboradorForm(request.POST or None, instance=colaborador)
    if form.is_valid():
        form.save()
        registrar(request, "Edição de dados", colaborador)
        messages.success(request, "Dados atualizados.")
        return redirect("detalhe_colaborador", colaborador.id)
    return render(request, "acessos/form.html", {"form": form, "titulo": f"Editar {colaborador}"})


@login_required
def detalhe_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    form = AcessoForm(colaborador=colaborador)
    contexto = {"colaborador": colaborador, "form": form,
                "acessos": colaborador.acessos.select_related("sistema")}
    return render(request, "acessos/colaborador.html", contexto)


@login_required
@require_POST
def conceder_acesso(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    if not colaborador.ativo:
        messages.error(request, "Não é possível dar acesso a quem já saiu da empresa.")
        return redirect("detalhe_colaborador", id)

    form = AcessoForm(request.POST, colaborador=colaborador)
    if form.is_valid():
        acesso = form.save(commit=False)
        acesso.colaborador = colaborador
        acesso.save()
        registrar(request, f"Acesso concedido ({acesso.get_nivel_display()})", colaborador, acesso.sistema)
        messages.success(request, f"Acesso ao {acesso.sistema} concedido.")
    return redirect("detalhe_colaborador", id)


@login_required
@require_POST
def revogar_acesso(request, id):
    acesso = get_object_or_404(Acesso, id=id)
    colaborador = acesso.colaborador
    registrar(request, "Acesso revogado", colaborador, acesso.sistema)
    acesso.delete()
    messages.success(request, f"Acesso ao {acesso.sistema} revogado.")
    return redirect("detalhe_colaborador", colaborador.id)


@login_required
@require_POST
def desligar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    # quando alguém sai da empresa, todos os acessos são retirados de uma vez.
    # antes isso dependia de alguém lembrar de tirar sistema por sistema
    for acesso in colaborador.acessos.select_related("sistema"):
        registrar(request, "Acesso revogado (desligamento)", colaborador, acesso.sistema)
    quantidade = colaborador.acessos.count()
    colaborador.acessos.all().delete()

    colaborador.ativo = False
    colaborador.save()
    registrar(request, "Desligamento", colaborador)
    messages.success(request, f"{colaborador} desligado(a). {quantidade} acesso(s) retirado(s).")
    return redirect("detalhe_colaborador", id)


@login_required
def lista_sistemas(request):
    form = SistemaForm(request.POST or None)
    if form.is_valid():
        sistema = form.save()
        messages.success(request, f"Sistema {sistema} cadastrado.")
        return redirect("sistemas")
    sistemas = Sistema.objects.all()
    return render(request, "acessos/sistemas.html", {"sistemas": sistemas, "form": form})


@login_required
def detalhe_sistema(request, id):
    # responde a pergunta "quem tem acesso a este sistema?"
    sistema = get_object_or_404(Sistema, id=id)
    acessos = sistema.acessos.select_related("colaborador")
    return render(request, "acessos/sistema.html", {"sistema": sistema, "acessos": acessos})


@login_required
def historico(request):
    registros = Registro.objects.select_related("feito_por")[:200]
    return render(request, "acessos/historico.html", {"registros": registros})
