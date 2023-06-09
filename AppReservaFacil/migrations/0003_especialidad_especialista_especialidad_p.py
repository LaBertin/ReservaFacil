# Generated by Django 4.0.2 on 2023-03-21 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0002_remove_especialista_id_especialista_id_especialista_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('Codigo_especialidad', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('Nombre_especialidad', models.CharField(max_length=256)),
                ('Icono_especialidad', models.ImageField(upload_to='')),
                ('Color_especialidad', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Docente',
                'verbose_name_plural': 'Docentes',
            },
        ),
        migrations.AddField(
            model_name='especialista',
            name='Especialidad_P',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AppReservaFacil.especialidad'),
        ),
    ]
