# Generated by Django 4.0.2 on 2023-04-27 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0037_rename_id_cita_su_citasinusuario_id_cita'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='Confirmacion_Cita_Operador',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='citasinusuario',
            name='Confirmacion_Cita_Operador',
            field=models.BooleanField(default=False),
        ),
    ]
