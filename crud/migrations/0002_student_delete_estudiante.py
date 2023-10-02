# Generated by Django 4.2.5 on 2023-10-01 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_code', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=100)),
                ('genre', models.CharField(choices=[('M', 'M - Masculino'), ('F', 'F - Femenino'), ('O', 'O - Otro')], max_length=1)),
                ('id_type', models.CharField(choices=[('PA', 'PA - Pasaporte'), ('CC', 'CC - Cédula de Ciudadanía'), ('TI', 'TI - Tarjeta de Identidad'), ('CE', 'CE - Cédula de Extranjería'), ('RC', 'RC - Registro Civil')], max_length=2)),
                ('id_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=1000)),
                ('institutional_email', models.EmailField(max_length=1000)),
                ('icfes_score', models.IntegerField()),
                ('birth_date', models.DateField()),
                ('cellphone_number', models.CharField(max_length=15)),
                ('accumulated_average', models.DecimalField(decimal_places=1, max_digits=2)),
                ('credits_studied', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Estudiante',
        ),
    ]
