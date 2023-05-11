# Generated by Django 4.1.7 on 2023-04-18 10:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("FMSApp", "0014_alter_inputmsched_typeofrepairandmaintenance"),
    ]

    operations = [
        migrations.AddField(
            model_name="inputddetail",
            name="PlateNumber",
            field=models.ForeignKey(
                default="7",
                on_delete=django.db.models.deletion.CASCADE,
                to="FMSApp.inputvdetail",
            ),
        ),
        migrations.AddField(
            model_name="inputdeploymentsched",
            name="PlateNumber",
            field=models.ForeignKey(
                default="7",
                on_delete=django.db.models.deletion.CASCADE,
                to="FMSApp.inputvdetail",
            ),
        ),
        migrations.AddField(
            model_name="inputmsched",
            name="PlateNumber",
            field=models.ForeignKey(
                default="7",
                on_delete=django.db.models.deletion.CASCADE,
                to="FMSApp.inputvdetail",
            ),
        ),
        migrations.AddField(
            model_name="inputvspecs",
            name="PlateNumber",
            field=models.ForeignKey(
                default="7",
                on_delete=django.db.models.deletion.CASCADE,
                to="FMSApp.inputvdetail",
            ),
        ),
        migrations.AlterField(
            model_name="inputdeploymentsched",
            name="Date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="inputmsched",
            name="Date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="inputvdetail",
            name="PlateNumber",
            field=models.CharField(default="abc-123", max_length=100, unique=True),
        ),
    ]
