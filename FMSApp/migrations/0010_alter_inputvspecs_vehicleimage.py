# Generated by Django 4.0.2 on 2023-03-30 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FMSApp', '0009_inputvspecs_vehicleimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputvspecs',
            name='VehicleImage',
            field=models.ImageField(default='', upload_to='static/Vehicle_Images'),
        ),
    ]
