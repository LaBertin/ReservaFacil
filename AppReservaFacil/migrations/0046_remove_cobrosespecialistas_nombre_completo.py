# Generated by Django 4.0.2 on 2023-04-28 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0045_cobrosespecialistas_nombre_completo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cobrosespecialistas',
            name='Nombre_completo',
        ),
    ]