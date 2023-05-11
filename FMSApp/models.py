import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User

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
    PlateNumber = models.CharField(max_length=100, unique=True)
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
        return str(self.pk) + ": " + self.PlateNumber + ", " + self.VehicleBrand + " , " + self.VehicleModel + ", " + self.GasConsumption
    

class InputVSpecs(models.Model):
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
    Date = models.DateField()
    TypeofRepairandMaintenance = models.CharField(max_length=300)
    objects = models.Manager()

    def __str__(self):
        return f"{self.date} - {self.repair}"
    
class InputDeploymentSched(models.Model):
    Date = models.DateField()
    DeploymentLocation = models.CharField(max_length=100)
    objects = models.Manager()


    def __str__(self):
        return f"{self.date} - {self.location}"
    
@receiver(post_save, sender=InputMSched)
def create_maintenance_notification(sender, instance, **kwargs):
    today = datetime.date.today().strftime("%Y-%m-%d")
    if instance.Date == today:
        title = 'Maintenance Schedule (Today)'
    else:
        title = 'Maintenance Schedule'
    description = f'{instance.TypeofRepairandMaintenance}  {instance.Date}'
    existing_task = Task.objects.filter(title=title, due_date=instance.Date, description=description)
    
    if(len(existing_task) > 0):
        return
    
    task = Task.objects.create(title=title, description=description, due_date=instance.Date)
    notification = Notification.objects.create(task=task)
    print ("category: '%s'" % instance.TypeofRepairandMaintenance)

@receiver(post_save, sender=InputDeploymentSched)
def create_deployment_notification(sender, instance, **kwargs):
    today = datetime.date.today().strftime("%Y-%m-%d")
    if instance.Date == today:        
        title = 'Maintenance Schedule (Today)'
    else:
        title = 'Maintenance Schedule'
    description = f'{instance.DeploymentLocation}  {instance.Date}'
    existing_task = Task.objects.filter(title=title, due_date=instance.Date, description=description)
    
    if(len(existing_task) > 0):
        return
    
    task = Task.objects.create(title=title, description=description, due_date=instance.Date)
    notification = Notification.objects.create(task=task)
    print ("category: '%s'" % instance.DeploymentLocation)
    
# for notif

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(unique=True)

    @property
    def remaining_days(self):
        remaining = (self.due_date - datetime.date.today()).days
        return remaining

class Notification(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, unique=True)
    opened = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

    