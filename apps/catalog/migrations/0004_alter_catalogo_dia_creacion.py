# Generated by Django 4.1 on 2022-08-12 17:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_catalogo_dia_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo',
            name='dia_creacion',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 12, 17, 34, 15, 973226, tzinfo=datetime.timezone.utc)),
        ),
    ]