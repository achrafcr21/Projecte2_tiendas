# Generated by Django 5.1.7 on 2025-03-23 14:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_negocio', models.CharField(max_length=200, verbose_name='Nom del negoci')),
                ('descripcion', models.TextField(verbose_name='Descripció del negoci')),
                ('email_contacto', models.EmailField(max_length=254, verbose_name='Email de contacte')),
                ('telefono', models.CharField(max_length=20, verbose_name='Telèfon')),
                ('fecha_solicitud', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data de sol·licitud')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendent de revisió'), ('aceptada', 'Sol·licitud acceptada'), ('rechazada', 'Sol·licitud rebutjada')], default='pendiente', max_length=20, verbose_name='Estat')),
                ('notas_admin', models.TextField(blank=True, null=True, verbose_name='Notes del admin')),
            ],
            options={
                'verbose_name': 'Sol·licitud',
                'verbose_name_plural': 'Sol·licituds',
                'db_table': 'solicitudes',
                'ordering': ['-fecha_solicitud'],
            },
        ),
    ]
