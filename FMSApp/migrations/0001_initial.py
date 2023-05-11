# Generated by Django 4.0.2 on 2023-01-31 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=300, unique=True)),
                ('password', models.CharField(max_length=300)),
                ('first_name', models.CharField(max_length=300)),
                ('last_name', models.CharField(max_length=300)),
                ('sex', models.CharField(max_length=300)),
            ],
        ),
    ]
