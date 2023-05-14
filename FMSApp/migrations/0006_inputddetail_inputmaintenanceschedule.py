# Generated by Django 4.0.2 on 2023-03-22 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FMSApp', '0005_inputvspecs'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputDDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DriversName', models.CharField(max_length=200)),
                ('DriversAge', models.CharField(max_length=100)),
                ('DriversMedicalCondtition', models.CharField(max_length=300)),
                ('DriversLicenseNumber', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='InputMaintenanceSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('TypeofRepairandMaintenance', models.CharField(max_length=300, unique=True)),
            ],
        ),
    ]