# Generated by Django 4.2.5 on 2023-11-28 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0029_alter_document_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=1000)),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(max_length=1000)),
                ('email', models.CharField(max_length=1000)),
                ('user_rol', models.CharField(choices=[('Bienestar Universitario', 'Bienestar Universitario'), ('Filantropía', 'Filantropía')], max_length=100)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
