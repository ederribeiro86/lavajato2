from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lavajato', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimento',
            name='finalizado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='movimento',
            name='hora_entrada',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
