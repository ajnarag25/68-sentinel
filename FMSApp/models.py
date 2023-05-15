from pickle import TRUE
from django.db import models
from django.utils.timezone import now
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=300, unique=True)
    password = models.CharField(max_length=300)
    objects = models.Manager()

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def __str__(self):
        return str(self.pk) + ": " + self.username


class InputVDetail(models.Model):
    PlateNumber = models.CharField(
        max_length=100, unique=True, default="abc-123")
    VehicleBrand = models.CharField(max_length=300)
    VehicleModel = models.CharField(max_length=300)
    GasConsumption = models.CharField(max_length=300)
    objects = models.Manager()

    def getPlateNumber(self):
        return self.PlateNumber

    def getVehicleBrand(self):
        return self.VehicleBrand

    def getVehicleModel(self):
        return self.VehicleModel

    def getGasConsumption(self):
        return self.GasConsumption

    def __str__(self):
        return str(self.pk) + ": " + self.PlateNumber


class InputVSpecs(models.Model):
    PlateNumber = models.ForeignKey(
        InputVDetail, on_delete=models.CASCADE, blank=True, null=True)
    ChassisNumber = models.CharField(max_length=100, unique=True)
    ACUCompany = models.CharField(max_length=300)
    WheelerType = models.CharField(max_length=300)
    Engine = models.CharField(max_length=200)
    VehicleImage = models.ImageField(upload_to='', default="")
    objects = models.Manager()

    def getChassisNumber(self):
        return self.ChassisNumber

    def getACUCompany(self):
        return self.ACUCompany

    def getWheelerType(self):
        return self.WheelerType

    def getEngine(self):
        return self.Engine

    def getVehicleImage(self):
        return self.VehicleImage

    def __str__(self):
        return str(self.pk) + ": " + self.ChassisNumber + ", " + self.ACUCompany + " , " + self.WheelerType + ", " + self.Engine


class InputDDetail(models.Model):
    PlateNumber = models.ForeignKey(
        InputVDetail, on_delete=models.CASCADE, blank=True, null=True)
    DriversName = models.CharField(max_length=200)
    DriversAge = models.CharField(max_length=100)
    DriversMedicalCondition = models.CharField(max_length=300)
    DriversLicenseNumber = models.CharField(max_length=300, unique=True)
    objects = models.Manager()

    def getDriversName(self):
        return self.DriversName

    def getDriversAge(self):
        return self.DriversAge

    def getDriversMedicalCondition(self):
        return self.DriversMedicalCondition

    def getDriversLicenseNumber(self):
        return self.DriversLicenseNumber

    def __str__(self):
        return str(self.pk) + ": " + self.DriversName + ", " + self.DriversAge + " , " + self.DriversMedicalCondition + ", " + self.DriversLicenseNumber


class InputMSched(models.Model):
    PlateNumber = models.ForeignKey(
        InputVDetail, on_delete=models.CASCADE, blank=True, null=True)
    Date = models.DateField(default=now)
    status = models.CharField(max_length=300,null=True)
    TypeofRepairandMaintenance = models.CharField(max_length=300, null=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.date} - {self.repair}"


class InputDeploymentSched(models.Model):
    PlateNumber = models.ForeignKey(
        InputVDetail, on_delete=models.CASCADE, blank=True, null=True)
    Date = models.DateTimeField(default=now)
    DeploymentLocation = models.CharField(max_length=100)
    objects = models.Manager()

    def __str__(self):
        return f"{self.date} - {self.location}"
    
class DateUpdated(models.Model):
    platenumber_id = models.IntegerField()
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.platenumber_id} - {self.date_updated}'