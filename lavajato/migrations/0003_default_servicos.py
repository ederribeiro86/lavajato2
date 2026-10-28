from django.db import migrations


def create_default_servicos(apps, schema_editor):
    Servico = apps.get_model('lavajato', 'Servico')
    servicos_padrao = [
        ('Lavagem Simples', '80.00', 'N'),
        ('Lavagem Premium', '180.00', 'S'),
        ('Lavagem Detalhada', '280.00', 'S'),
    ]

    for descricao, valor, fidelidade in servicos_padrao:
        Servico.objects.get_or_create(
            descricao=descricao,
            defaults={'valor': valor, 'fidelidade': fidelidade},
        )


class Migration(migrations.Migration):
    dependencies = [
        ('lavajato', '0002_movimento_hora_entrada_movimento_finalizado'),
    ]

    operations = [
        migrations.RunPython(create_default_servicos, migrations.RunPython.noop),
    ]
