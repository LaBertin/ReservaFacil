# Generated by Django 4.0.2 on 2023-05-04 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0049_merge_20230503_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cobro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ID_Cobro', models.IntegerField()),
                ('Rut_Pac_Cobro', models.CharField(max_length=9, null=True)),
                ('Estado_cobro', models.CharField(choices=[('Pagado', 'Pagado'), ('Por pagar', 'Por pagar')], max_length=10, null=True)),
                ('Especialidad_Cobro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='AppReservaFacil.especialidad')),
                ('Especialista_Cobro', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='AppReservaFacil.especialista')),
                ('Monto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='AppReservaFacil.cobrosespecialistas')),
            ],
        ),
    ]
