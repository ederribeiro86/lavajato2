from django.test import TestCase
from django.urls import reverse

from .forms import MovimentoForm
from .models import Movimento, PessoaFisica, PessoaJuridica, Servico, Veiculo


class CadastroPessoaTests(TestCase):
    def test_cadastro_pessoa_fisica(self):
        response = self.client.post(
            reverse('cadastro_pessoa'),
            {
                'tipo_pessoa': 'F',
                'nome': 'Maria Silva',
                'endereco': 'Rua das Flores, 123',
                'email': 'maria@email.com',
                'celular': '11999999999',
                'cpf': '12345678901',
                'data_nascimento': '1990-01-15',
                'identidade': '123456789',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(PessoaFisica.objects.filter(cpf='12345678901').exists())

    def test_cadastro_pessoa_juridica(self):
        response = self.client.post(
            reverse('cadastro_pessoa'),
            {
                'tipo_pessoa': 'J',
                'nome': 'Empresa Teste LTDA',
                'endereco': 'Av. Principal, 500',
                'email': 'empresa@email.com',
                'celular': '1133334444',
                'cnpj': '12345678000199',
                'contato_nome': 'João da Empresa',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(PessoaJuridica.objects.filter(cnpj='12345678000199').exists())

    def test_dashboard_exibe_alerta_de_lavagem_pendente(self):
        pessoa = PessoaFisica.objects.create(
            nome='Cliente Lavagem',
            endereco='Rua A',
            celular='11988887777',
            cpf='11122233344',
        )
        veiculo = Veiculo.objects.create(
            pessoa=pessoa,
            placa='ABC1234',
            tipo='Sedan',
            modelo='Gol',
            cor='Preto',
        )
        servico = Servico.objects.create(
            descricao='Lavagem completa',
            valor='120.00',
            fidelidade='N',
        )
        Movimento.objects.create(
            veiculo=veiculo,
            servico=servico,
            data='2026-09-17',
            hora='08:30:00',
            hora_entrada='08:30:00',
            valor='120.00',
            pagamento='N',
            finalizado=False,
        )

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['alerta_finalizacao'])
        self.assertIn('Lavagem em andamento', response.content.decode('utf-8'))

    def test_movimentacao_caixa_registra_novo_movimento(self):
        pessoa = PessoaFisica.objects.create(
            nome='Cliente Caixa',
            endereco='Rua B',
            celular='11977776666',
            cpf='22233344455',
        )
        veiculo = Veiculo.objects.create(
            pessoa=pessoa,
            placa='XYZ9876',
            tipo='SUV',
            modelo='Civic',
            cor='Branco',
        )
        servico = Servico.objects.create(
            descricao='Detalhamento',
            valor='180.00',
            fidelidade='S',
        )

        response = self.client.post(
            reverse('movimentacao_caixa'),
            {
                'veiculo': veiculo.placa,
                'servico': servico.id,
                'data': '2026-09-17',
                'hora': '09:15',
                'hora_entrada': '09:15',
                'valor': '180.00',
                'pagamento': 'S',
                'data_pagto': '2026-09-17',
                'finalizado': 'on',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Movimento.objects.filter(veiculo=veiculo, servico=servico).exists())

    def test_servicos_padrao_existem(self):
        servicos_esperados = ['Lavagem Simples', 'Lavagem Premium', 'Lavagem Detalhada']

        for descricao in servicos_esperados:
            self.assertTrue(
                Servico.objects.filter(descricao=descricao).exists(),
                f'O serviço padrão "{descricao}" não foi criado.'
            )

    def test_formulario_de_movimento_exibe_veiculo_e_servico_vinculados(self):
        pessoa = PessoaFisica.objects.create(
            nome='Cliente Vínculo',
            endereco='Rua C',
            celular='11955554444',
            cpf='33344455566',
        )
        veiculo = Veiculo.objects.create(
            pessoa=pessoa,
            placa='BRA2025',
            tipo='Hatch',
            modelo='Fiat Uno',
            cor='Azul',
        )
        servico = Servico.objects.create(
            descricao='Lavagem premium',
            valor='220.00',
            fidelidade='S',
        )

        form = MovimentoForm()
        veiculo_widget = form['veiculo'].as_widget()
        servico_widget = form['servico'].as_widget()

        self.assertIn(f'value="{veiculo.placa}"', veiculo_widget)
        self.assertIn(f'Fiat Uno ({veiculo.placa})', veiculo_widget)
        self.assertIn(servico.descricao, servico_widget)
