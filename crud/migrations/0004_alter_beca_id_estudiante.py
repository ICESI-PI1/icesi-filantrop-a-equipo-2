# Generated by Django 4.2.5 on 2023-10-09 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0003_beca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beca',
            name='id_estudiante',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
