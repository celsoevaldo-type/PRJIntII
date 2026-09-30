from django import forms

from .models import Acesso, Colaborador, Sistema


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ["nome", "email", "cargo", "setor", "data_entrada"]
        widgets = {"data_entrada": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}


class SistemaForm(forms.ModelForm):
    class Meta:
        model = Sistema
        fields = ["nome", "descricao"]


class AcessoForm(forms.ModelForm):
    class Meta:
        model = Acesso
        fields = ["sistema", "nivel"]

    def __init__(self, *args, colaborador=None, **kwargs):
        super().__init__(*args, **kwargs)
        # na lista só aparecem os sistemas que a pessoa ainda não tem
        if colaborador:
            ja_tem = colaborador.acessos.values_list("sistema_id", flat=True)
            self.fields["sistema"].queryset = Sistema.objects.exclude(id__in=ja_tem)
