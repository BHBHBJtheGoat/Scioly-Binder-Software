# Generated by Django 5.0.7 on 2024-08-17 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_bindermodel_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bindermodel',
            name='content',
            field=models.JSONField(blank=True),
        ),
    ]
