# Generated by Django 4.2.5 on 2023-10-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0010_alter_beca_id_estudiante'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beca',
            old_name='tipo',
            new_name='tipo_beca',
        ),
        migrations.AlterField(
            model_name='beca',
            name='id_estudiante',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='beca',
            name='monto',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
