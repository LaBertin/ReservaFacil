# Generated by Django 4.0.2 on 2023-04-26 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0035_merge_20230425_1733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paciente',
            options={'verbose_name': 'Paciente', 'verbose_name_plural': 'Pacientes'},
        ),
        migrations.RemoveField(
            model_name='ficha_medica',
            name='Med_Tom_Actu',
        ),
        migrations.AddField(
            model_name='ficha_medica',
            name='Observaciones_Ficha',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='ficha_medica',
            name='Alimentos_TI',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='ficha_medica',
            name='Ani_Ins_TI',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='ficha_medica',
            name='Antibioticos_TI',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='ficha_medica',
            name='Enf_Cronic_TI',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='ficha_medica',
            name='Grupo_Sanguineo',
            field=models.CharField(choices=[('Ninguno', 'Ninguno'), ('Amas', 'A+'), ('Omas', 'O+'), ('Bmas', 'B+'), ('ABmas', 'AB+'), ('Amenos', 'A-'), ('Omenos', 'O-'), ('Bmenos', 'B-'), ('ABmenos', 'AB-')], max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='ficha_medica',
            name='Medicamentos_TI',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='ficha_medica',
            name='RUT_Pac',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='ficha_medica',
            name='Sis_Sal_Pac',
            field=models.CharField(choices=[('Ninguno', 'Ninguno'), ('SegCom', 'Seguro Complementario'), ('ISAPRE', 'ISAPRE'), ('FONASA', 'FONASA'), ('FFAA', 'Fuerzas Armadas')], max_length=21, null=True),
        ),
    ]