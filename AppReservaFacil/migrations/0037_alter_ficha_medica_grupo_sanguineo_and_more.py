# Generated by Django 4.0.2 on 2023-04-26 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0036_alter_paciente_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficha_medica',
            name='Grupo_Sanguineo',
            field=models.CharField(choices=[('Ninguno', 'Ninguno'), ('A+', 'A+'), ('O+', 'O+'), ('B+', 'B+'), ('AB+', 'AB+'), ('A-', 'A-'), ('O-', 'O-'), ('B-', 'B-'), ('AB-', 'AB-')], max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='ficha_medica',
            name='Sis_Sal_Pac',
            field=models.CharField(choices=[('Ninguno', 'Ninguno'), ('Seguro Complementario', 'Seguro Complementario'), ('ISAPRE', 'ISAPRE'), ('FONASA', 'FONASA'), ('Fuerzas Armadas', 'Fuerzas Armadas')], max_length=21, null=True),
        ),
    ]