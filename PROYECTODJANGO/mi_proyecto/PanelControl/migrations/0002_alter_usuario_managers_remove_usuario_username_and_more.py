# Generated by Django 5.1.4 on 2024-12-06 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PanelControl', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usuario',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='username',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
