from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import MovimentoForm, PessoaForm, ServicoForm, VeiculoForm
from .models import Movimento, Pessoa, Servico, Veiculo


def home(request):
    return render(request, 'lavajato/index.html')


def dashboard(request):
    clientes = Pessoa.objects.count()
    veiculos = Veiculo.objects.count()
    servicos = Servico.objects.count()
    movimentacoes = Movimento.objects.count()
    faturamento_total = sum((mov.valor for mov in Movimento.objects.all()), Decimal('0.00'))
    pagamentos_confirmados = Movimento.objects.filter(pagamento='S').count()
    pagamentos_pendentes = Movimento.objects.filter(pagamento='N').count()
    ultimos_movimentos = Movimento.objects.select_related('veiculo', 'servico').order_by('-data', '-hora')[:5]
    lavagens_em_andamento = Movimento.objects.select_related('veiculo', 'servico').filter(finalizado=False).order_by('-data', '-hora_entrada')[:5]
    alerta_finalizacao = lavagens_em_andamento.exists()

    context = {
        'clientes': clientes,
        'veiculos': veiculos,
        'servicos': servicos,
        'movimentacoes': movimentacoes,
        'faturamento_total': faturamento_total,
        'pagamentos_confirmados': pagamentos_confirmados,
        'pagamentos_pendentes': pagamentos_pendentes,
        'ultimos_movimentos': ultimos_movimentos,
        'lavagens_em_andamento': lavagens_em_andamento,
        'alerta_finalizacao': alerta_finalizacao,
    }
    return render(request, 'lavajato/dashboard.html', context)


def movimentacao_caixa(request):
    if request.method == 'POST':
        form = MovimentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimentação registrada com sucesso!')
            return redirect('movimentacao_caixa')
    else:
        form = MovimentoForm()

    movimentos = Movimento.objects.select_related('veiculo', 'servico').order_by('-data', '-hora')[:10]

    total_caixa = sum((mov.valor for mov in Movimento.objects.all()), Decimal('0.00'))
    total_servicos = sum((mov.valor for mov in Movimento.objects.all()), Decimal('0.00'))
    quantidade = movimentos.count()

    context = {
        'form': form,
        'movimentos': movimentos,
        'total_caixa': total_caixa,
        'total_servicos': total_servicos,
        'quantidade': quantidade,
    }
    return render(request, 'lavajato/movimentacao_caixa.html', context)


def cadastro_pessoa(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cadastro_pessoa')
    else:
        form = PessoaForm()

    return render(request, 'lavajato/cadastro_pessoa.html', {'form': form})


def listar_pessoas(request):
    pessoas = Pessoa.objects.all().order_by('nome')
    return render(request, 'lavajato/lista_pessoas.html', {'pessoas': pessoas})


def cadastro_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('cadastro_veiculo')
    else:
        form = VeiculoForm()

    return render(request, 'lavajato/cadastro_veiculo.html', {'form': form})


def listar_veiculos(request):
    veiculos = Veiculo.objects.select_related('pessoa').all().order_by('modelo')
    return render(request, 'lavajato/lista_veiculos.html', {'veiculos': veiculos})


def cadastro_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço cadastrado com sucesso!')
            return redirect('cadastro_servico')
    else:
        form = ServicoForm()

    return render(request, 'lavajato/cadastro_servico.html', {'form': form})


def listar_servicos(request):
    servicos = Servico.objects.all().order_by('descricao')
    return render(request, 'lavajato/lista_servicos.html', {'servicos': servicos})
