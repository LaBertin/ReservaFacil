# Generated by Django 4.2 on 2023-04-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0014_alter_especialista_dia_esp_c_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='Dia_Esp_C',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='Dia_Esp_P',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='Dia_Esp_S',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='Dia_Esp_T',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
