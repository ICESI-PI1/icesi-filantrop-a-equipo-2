# Generated by Django 4.2.5 on 2023-10-09 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0006_alter_beca_id_estudiante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beca',
            name='id_estudiante',
            field=models.CharField(max_length=255),
        ),
    ]
