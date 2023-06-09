# Generated by Django 4.0.2 on 2023-04-13 15:38

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('AppReservaFacil', '0016_alter_especialista_minutes_esp_c_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='especialista',
            name='Dia_Esp_C',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('lun', 'Lunes'), ('mar', 'Martes'), ('mie', 'Miercoles'), ('jue', 'Jueves'), ('vie', 'Viernes'), ('sab', 'Sabado'), ('dom', 'Domingo')], max_length=27, null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='Dia_Esp_P',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('lun', 'Lunes'), ('mar', 'Martes'), ('mie', 'Miercoles'), ('jue', 'Jueves'), ('vie', 'Viernes'), ('sab', 'Sabado'), ('dom', 'Domingo')], max_length=27, null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='Dia_Esp_S',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('lun', 'Lunes'), ('mar', 'Martes'), ('mie', 'Miercoles'), ('jue', 'Jueves'), ('vie', 'Viernes'), ('sab', 'Sabado'), ('dom', 'Domingo')], max_length=27, null=True),
        ),
        migrations.AlterField(
            model_name='especialista',
            name='Dia_Esp_T',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('lun', 'Lunes'), ('mar', 'Martes'), ('mie', 'Miercoles'), ('jue', 'Jueves'), ('vie', 'Viernes'), ('sab', 'Sabado'), ('dom', 'Domingo')], max_length=27, null=True),
        ),
    ]
