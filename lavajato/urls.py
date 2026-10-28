from django.urls import path
from .views import (
    cadastro_pessoa,
    cadastro_servico,
    cadastro_veiculo,
    dashboard,
    home,
    listar_pessoas,
    listar_servicos,
    listar_veiculos,
    movimentacao_caixa,
)

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cadastro/', cadastro_pessoa, name='cadastro_pessoa'),
    path('lista/', listar_pessoas, name='listar_pessoas'),
    path('veiculo/cadastro/', cadastro_veiculo, name='cadastro_veiculo'),
    path('veiculo/lista/', listar_veiculos, name='listar_veiculos'),
    path('servico/cadastro/', cadastro_servico, name='cadastro_servico'),
    path('servico/lista/', listar_servicos, name='listar_servicos'),
    path('movimentacao-caixa/', movimentacao_caixa, name='movimentacao_caixa'),
]
