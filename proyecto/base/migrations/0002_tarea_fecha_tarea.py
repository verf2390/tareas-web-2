# Generated by Django 5.1.7 on 2025-07-18 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='fecha_tarea',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
