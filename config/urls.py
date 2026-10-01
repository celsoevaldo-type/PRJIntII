from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

# Arquivo de roteamento (rotas em preset)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("entrar/", auth_views.LoginView.as_view(template_name="acessos/login.html"), name="login"),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("acessos.urls")),
]
