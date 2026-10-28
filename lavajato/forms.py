from django import forms
from .models import Movimento, Pessoa, PessoaFisica, PessoaJuridica, Servico, Veiculo


class MovimentoForm(forms.ModelForm):
    veiculo = forms.ModelChoiceField(
        queryset=Veiculo.objects.select_related('pessoa').order_by('modelo', 'placa'),
        empty_label='Selecione uma opção',
        label='Veículo',
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='placa',
    )
    servico = forms.ModelChoiceField(
        queryset=Servico.objects.order_by('descricao'),
        empty_label='Selecione uma opção',
        label='Serviço',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Movimento
        fields = ['veiculo', 'servico', 'data', 'hora', 'hora_entrada', 'valor', 'pagamento', 'data_pagto', 'finalizado']
        labels = {
            'data': 'Data',
            'hora': 'Hora de saída',
            'hora_entrada': 'Hora de entrada',
            'valor': 'Valor',
            'pagamento': 'Pagamento',
            'data_pagto': 'Data do pagamento',
            'finalizado': 'Lavagem finalizada',
        }
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_entrada': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pagamento': forms.Select(choices=[('', 'Selecione uma opção'), ('S', 'Sim'), ('N', 'Não')], attrs={'class': 'form-control'}),
            'data_pagto': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'finalizado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def label_from_instance(self, obj):
        if isinstance(obj, Veiculo):
            return f'{obj.modelo} / {obj.placa}'
        return str(obj)


class PessoaForm(forms.Form):
    TIPOS_PESSOA = [
        ('', 'Selecione uma opção'),
        ('F', 'Pessoa física'),
        ('J', 'Pessoa jurídica'),
    ]

    tipo_pessoa = forms.ChoiceField(
        choices=TIPOS_PESSOA,
        required=True,
        label='Tipo de pessoa',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    nome = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nome')
    endereco = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Endereço')
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}), label='E-mail')
    celular = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Celular')
    credito = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Crédito')
    cpf = forms.CharField(required=False, max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}), label='CPF')
    data_nascimento = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Data de nascimento')
    identidade = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Identidade')
    cnpj = forms.CharField(required=False, max_length=14, widget=forms.TextInput(attrs={'class': 'form-control'}), label='CNPJ')
    contato_nome = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nome do contato')

    def clean(self):
        cleaned_data = super().clean()
        tipo_pessoa = cleaned_data.get('tipo_pessoa')

        if tipo_pessoa == 'F':
            if not cleaned_data.get('cpf'):
                self.add_error('cpf', 'Informe o CPF.')
            if cleaned_data.get('cnpj'):
                cleaned_data['cnpj'] = ''
        elif tipo_pessoa == 'J':
            if not cleaned_data.get('cnpj'):
                self.add_error('cnpj', 'Informe o CNPJ.')
            if cleaned_data.get('cpf'):
                cleaned_data['cpf'] = ''

        return cleaned_data

    def save(self, commit=True):
        tipo_pessoa = self.cleaned_data['tipo_pessoa']
        dados = self.cleaned_data.copy()
        dados.pop('tipo_pessoa')

        if tipo_pessoa == 'F':
            pessoa = PessoaFisica.objects.create(
                nome=dados['nome'],
                endereco=dados['endereco'],
                email=dados.get('email') or None,
                celular=dados['celular'],
                credito=dados.get('credito'),
                cpf=dados['cpf'],
                data_nascimento=dados.get('data_nascimento'),
                identidade=dados.get('identidade') or None,
            )
            return pessoa

        pessoa = PessoaJuridica.objects.create(
            nome=dados['nome'],
            endereco=dados['endereco'],
            email=dados.get('email') or None,
            celular=dados['celular'],
            credito=dados.get('credito'),
            cnpj=dados['cnpj'],
            contato_nome=dados.get('contato_nome') or None,
        )
        return pessoa


class VeiculoForm(forms.ModelForm):
    pessoa = forms.ModelChoiceField(
        queryset=Pessoa.objects.order_by('nome'),
        empty_label='Selecione uma opção',
        label='Cliente',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Veiculo
        fields = ['pessoa', 'placa', 'tipo', 'modelo', 'cor']
        labels = {
            'placa': 'Placa',
            'tipo': 'Tipo',
            'modelo': 'Modelo',
            'cor': 'Cor',
        }
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['descricao', 'valor', 'fidelidade']
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor',
            'fidelidade': 'Possui fidelidade?',
        }
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'fidelidade': forms.Select(choices=[('', 'Selecione uma opção'), ('S', 'Sim'), ('N', 'Não')], attrs={'class': 'form-control'}),
        }
