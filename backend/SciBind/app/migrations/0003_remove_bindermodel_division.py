# Generated by Django 5.0.7 on 2024-08-17 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_bindermodel_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bindermodel',
            name='division',
        ),
    ]
