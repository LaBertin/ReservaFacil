# Generated by Django 4.0.2 on 2023-05-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0066_cita_metodo_pago_cita'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='Metodo_Pago_Cita',
            field=models.CharField(choices=[('Particular', 'Particular'), ('Fonasa', 'Fonasa'), ('Isapre', 'Isapre'), ('Convenio', 'Convenio'), ('Otros', 'Otros')], max_length=10, null=True),
        ),
    ]
