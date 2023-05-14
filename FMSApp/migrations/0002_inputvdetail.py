# Generated by Django 4.0.2 on 2023-02-02 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FMSApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputVDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlateNumber', models.CharField(max_length=6, unique=True)),
                ('VehicleBrand', models.CharField(max_length=300)),
                ('VehicleModel', models.CharField(max_length=300)),
                ('GasConsumption', models.CharField(max_length=300)),
            ],
        ),
    ]