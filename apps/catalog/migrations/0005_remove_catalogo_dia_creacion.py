# Generated by Django 4.1 on 2022-08-12 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_catalogo_dia_creacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogo',
            name='dia_creacion',
        ),
    ]
