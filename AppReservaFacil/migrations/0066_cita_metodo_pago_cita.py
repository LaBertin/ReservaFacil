# Generated by Django 4.0.2 on 2023-05-23 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0065_alter_examene_fecha_nac_pac_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='Metodo_Pago_Cita',
            field=models.CharField(choices=[('Pagado', 'Pagado'), ('Por pagar', 'Por pagar')], max_length=10, null=True),
        ),
    ]
