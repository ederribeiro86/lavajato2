from django.contrib import admin
from .models import PessoaFisica, PessoaJuridica, Veiculo, Servico, Movimento

@admin.register(PessoaFisica)
class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'celular', 'credito')
    search_fields = ('nome', 'cpf')

@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'contato_nome', 'celular')
    search_fields = ('nome', 'cnpj')

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'modelo', 'tipo', 'pessoa', 'ultima_lavagem')
    search_fields = ('placa', 'modelo')
    list_filter = ('tipo',)

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'fidelidade')
    list_filter = ('fidelidade',)

@admin.register(Movimento)
class MovimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'veiculo', 'servico', 'data', 'hora', 'valor', 'pagamento')
    list_filter = ('pagamento', 'data', 'servico')
    date_hierarchy = 'data'
