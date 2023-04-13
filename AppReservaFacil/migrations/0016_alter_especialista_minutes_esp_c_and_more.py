# Generated by Django 4.2 on 2023-04-13 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0015_alter_especialista_dia_esp_c_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='Minutes_Esp_C',
            field=models.IntegerField(choices=[(15, '15 Minutos'), (30, '30 Minutos'), (45, '45 Minutos'), (60, '60 Minutos')], null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='Minutes_Esp_P',
            field=models.IntegerField(choices=[(15, '15 Minutos'), (30, '30 Minutos'), (45, '45 Minutos'), (60, '60 Minutos')], null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='Minutes_Esp_S',
            field=models.IntegerField(choices=[(15, '15 Minutos'), (30, '30 Minutos'), (45, '45 Minutos'), (60, '60 Minutos')], null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='Minutes_Esp_T',
            field=models.IntegerField(choices=[(15, '15 Minutos'), (30, '30 Minutos'), (45, '45 Minutos'), (60, '60 Minutos')], null=True),
        ),
    ]