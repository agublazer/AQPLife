# Generated by Django 2.2 on 2019-11-05 16:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_auto_20191102_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='hora',
            field=models.TimeField(default=datetime.time(11, 11, 40, 772710)),
        ),
        migrations.CreateModel(
            name='PaqueteActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Actividad')),
                ('id_paquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.Paquete')),
            ],
        ),
    ]