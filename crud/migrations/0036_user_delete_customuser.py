# Generated by Django 4.2.5 on 2023-11-28 07:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('crud', '0035_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(default='username', max_length=1000)),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(max_length=1000)),
                ('email', models.CharField(max_length=1000)),
                ('user_type', models.CharField(choices=[('Bienestar Universitario', 'Bienestar Universitario'), ('Filantropía', 'Filantropía')], max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(related_name='crud_users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='crud_users_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
