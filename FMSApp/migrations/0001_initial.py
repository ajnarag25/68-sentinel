# Generated by Django 4.2 on 2023-04-25 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InputDDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DriversName', models.CharField(max_length=200)),
                ('DriversAge', models.CharField(max_length=100)),
                ('DriversMedicalCondition', models.CharField(max_length=300)),
                ('DriversLicenseNumber', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='InputDeploymentSched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('DeploymentLocation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='InputMSched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('TypeofRepairandMaintenance', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='InputVDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PlateNumber', models.CharField(max_length=100, unique=True)),
                ('VehicleBrand', models.CharField(max_length=300)),
                ('VehicleModel', models.CharField(max_length=300)),
                ('GasConsumption', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='InputVSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ChassisNumber', models.CharField(max_length=100, unique=True)),
                ('ACUCompany', models.CharField(max_length=300)),
                ('WheelerType', models.CharField(max_length=300)),
                ('Engine', models.CharField(max_length=200)),
                ('VehicleImage', models.ImageField(default='', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('due_date', models.DateField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=300, unique=True)),
                ('password', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opened', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FMSApp.task', unique=True)),
            ],
        ),
    ]