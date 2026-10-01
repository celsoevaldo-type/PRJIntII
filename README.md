# Controle de Acessos

Projeto Integrador em Computação II – Univesp

Sistema web simples para uma pequena empresa saber quem tem acesso a cada sistema.
Dá para cadastrar colaboradores e sistemas, liberar e retirar acessos e, quando alguém
sai da empresa, retirar todos os acessos dessa pessoa de uma vez. Tudo fica no histórico.

## Como rodar

Precisa ter o Python 3 instalado.

```
pip install -r requirements.txt
python manage.py migrate
python manage.py popular
python manage.py runserver
```

Abra http://127.0.0.1:8000 no navegador e entre com:

- usuário: `admin`
- senha: `admin123`

O comando `popular` cria esse usuário e alguns dados de exemplo (todos fictícios).

Para rodar os testes:

```
python manage.py test acessos
```

## Sobre o código

Feito em Django, com Bootstrap e um pouco de JavaScript.

- `acessos/models.py` – as tabelas: Colaborador, Sistema, Acesso e Registro (histórico)
- `acessos/views.py` – o que cada tela faz (o desligamento está em `desligar_colaborador`)
- `acessos/templates/acessos/` – o HTML das telas
- `acessos/static/acessos/` – JavaScript (busca nas tabelas e confirmação) e CSS
- `acessos/tests.py` – testes das regras principais

O sistema não guarda senhas de outros sistemas, só registra quem pode acessar o quê.
A senha `admin123` é só para demonstração.
