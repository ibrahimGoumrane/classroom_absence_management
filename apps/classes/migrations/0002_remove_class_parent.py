# Generated by Django 5.1.7 on 2025-03-11 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='parent',
        ),
    ]
