# Generated by Django 4.2.5 on 2023-11-13 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0019_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='title',
        ),
    ]
