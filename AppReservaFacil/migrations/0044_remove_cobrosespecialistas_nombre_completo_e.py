# Generated by Django 4.0.2 on 2023-04-28 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0043_cobrosespecialistas_nombre_completo_e'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cobrosespecialistas',
            name='Nombre_completo_E',
        ),
    ]
