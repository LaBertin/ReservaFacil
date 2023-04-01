# Generated by Django 4.0.2 on 2023-03-31 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0006_cita_confirmacion_cita'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='Fecha_Cita',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='ID_Cita',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
