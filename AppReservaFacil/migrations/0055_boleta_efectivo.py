# Generated by Django 4.0.2 on 2023-05-09 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0054_boleta_arancel_boleta_num_documento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='boleta',
            name='Efectivo',
            field=models.IntegerField(null=True),
        ),
    ]
