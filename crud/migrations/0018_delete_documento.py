# Generated by Django 4.2.5 on 2023-11-13 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0017_remove_documento_student_documento_student_code'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Documento',
        ),
    ]
