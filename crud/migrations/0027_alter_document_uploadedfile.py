# Generated by Django 4.2.5 on 2023-11-22 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0026_alter_document_uploadedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uploadedFile',
            field=models.FileField(upload_to='./crud/static/reports/'),
        ),
    ]
