# Generated by Django 4.0.2 on 2023-04-25 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0036_rename_id_cita_citasinusuario_id_cita_su'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citasinusuario',
            old_name='ID_Cita_SU',
            new_name='ID_Cita',
        ),
    ]
