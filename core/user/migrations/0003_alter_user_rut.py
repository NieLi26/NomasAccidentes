# Generated by Django 4.0.1 on 2022-06-17 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_turno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rut',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Rut'),
        ),
    ]
