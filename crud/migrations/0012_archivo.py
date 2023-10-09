# Generated by Django 4.2.5 on 2023-10-09 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0011_rename_tipo_beca_tipo_beca_alter_beca_id_estudiante_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('peso', models.IntegerField()),
                ('archivo', models.FileField(upload_to='archivos/')),
            ],
        ),
    ]