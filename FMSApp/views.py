from django.shortcuts import render, get_object_or_404, redirect
from .models import InputDeploymentSched, User, InputVDetail, InputVSpecs, InputDDetail, InputMSched, Task, Notification
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.db.models import Q
# for notif thingy
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
from django.core.mail import send_mail
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

import csv


def exportVDetails(request):
    vdetails = InputVDetail.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=vdetails_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Plate Number', 'Vehicle Brand',
                    'Vehicle Model', 'Gas Consumption'])
    vdetails_fields = vdetails.values_list(
        'PlateNumber', 'VehicleBrand', 'VehicleModel', 'GasConsumption')
    for vdetail in vdetails_fields:
        writer.writerow(vdetail)
    return response


def exportDDetails(request):
    ddetails = InputDDetail.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=ddetails_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Driver Name', 'Driver Age',
                    'Medical Condition', 'License Number'])
    ddetails_fields = ddetails.values_list(
        'DriversName', 'DriversAge', 'DriversMedicalCondition', 'DriversLicenseNumber')
    for ddetail in ddetails_fields:
        writer.writerow(ddetail)
    return response


def exportVSpecs(request):
    vspecs = InputVSpecs.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=ddetails_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Chassis Number', 'ACU Company',
                    'Wheeler Type', 'Engine', 'Vehicle Image/s'])
    vspecs_fields = vspecs.values_list(
        'ChassisNumber', 'ACUCompany', 'WheelerType', 'Engine', 'VehicleImage')
    for vspec in vspecs_fields:
        writer.writerow(vspec)
    return response


def login(request):
    if (request.method == "POST"):
        u = User.objects.all()
        usernameInput = request.POST.get('uN')
        passwordInput = request.POST.get('pW')
        if (u.filter(username=usernameInput)) and (u.filter(password=passwordInput)):
            usr = get_object_or_404(
                User, username=usernameInput, password=passwordInput)
            request.session['user'] = usr.username
            request.session['userPK'] = usr.pk
            return redirect('main_menu')
        else:
            return render(request, 'FMSApp/login.html', {'invalidLogin': 'Incorrect Username or Password'})
    else:
        return render(request, 'FMSApp/login.html')


def main_menu(request):
    vdetails = InputVDetail.objects.all()
    context = {
        'vdetails': vdetails,
    }
    return render(request, 'FMSApp/main_menu.html', context=context)


def logout(request):
    del request.session['user']
    return render(request, 'FMSApp/login.html')


def Input_VDetails(request):
    d = InputVDetail.objects.all()
    if (request.method == "POST"):
        PlateNumberInput = request.POST.get('pN')
        VehicleBrandInput = request.POST.get('vB')
        VehicleModelInput = request.POST.get('vM')
        GasConsumptionInput = request.POST.get('gC')
        InputVDetail.objects.create(PlateNumber=PlateNumberInput, VehicleBrand=VehicleBrandInput,
                                    VehicleModel=VehicleModelInput, GasConsumption=GasConsumptionInput)
    return render(request, 'FMSApp/Input_VDetails.html')


def Input_VSpecs(request):
    d = InputVSpecs.objects.all()
    if (request.method == "POST") and request.FILES['upload']:
        ChassisNumberInput = request.POST.get('cN')
        ACUCompanyInput = request.POST.get('aC')
        WheelerTypeInput = request.POST.get('wT')
        EngineInput = request.POST.get('eG')
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        InputVSpecs.objects.create(ChassisNumber=ChassisNumberInput, ACUCompany=ACUCompanyInput,
                                   WheelerType=WheelerTypeInput, Engine=EngineInput, VehicleImage=upload)
        return render(request, 'FMSApp/Input_VSpecs.html', {'file_url': file_url})
    return render(request, 'FMSApp/Input_VSpecs.html')


def Input_DDetails(request):
    d = InputDDetail.objects.all()
    if (request.method == "POST"):
        DriverNameInput = request.POST.get('dN')
        DriverAgeInput = request.POST.get('dA')
        MedicalConditionInput = request.POST.get('mC')
        LicenseNumberInput = request.POST.get('lN')
        InputDDetail.objects.create(DriversName=DriverNameInput, DriversAge=DriverAgeInput,
                                    DriversMedicalCondition=MedicalConditionInput, DriversLicenseNumber=LicenseNumberInput)
    return render(request, 'FMSApp/Input_DDetails.html')


def SearchResults(request):
    if request.method == "POST":
        page = request.POST.get('page')
        searched = request.POST['searched']
        if page == 'A':
            vdetails = InputVDetail.objects.filter(PlateNumber__icontains=searched) | InputVDetail.objects.filter(
                VehicleBrand__icontains=searched) | InputVDetail.objects.filter(VehicleModel__icontains=searched) | InputVDetail.objects.filter(GasConsumption__icontains=searched)
            ddetails = InputDDetail.objects.filter(DriversName__icontains=searched) | InputDDetail.objects.filter(DriversAge__icontains=searched) | InputDDetail.objects.filter(
                DriversMedicalCondition__icontains=searched) | InputDDetail.objects.filter(DriversLicenseNumber__icontains=searched)
            vspecs = InputVSpecs.objects.filter(ChassisNumber__icontains=searched) | InputVSpecs.objects.filter(
                ACUCompany__icontains=searched) | InputVSpecs.objects.filter(WheelerType__icontains=searched) | InputVSpecs.objects.filter(Engine__icontains=searched)
            return render(request, 'FMSApp/SearchResults.html', {'searched': searched, 'vdetails': vdetails, 'ddetails': ddetails, 'vspecs': vspecs})
        elif page == "VD":
            vdetails = InputVDetail.objects.filter(PlateNumber__icontains=searched) | InputVDetail.objects.filter(
                VehicleBrand__icontains=searched) | InputVDetail.objects.filter(VehicleModel__icontains=searched) | InputVDetail.objects.filter(GasConsumption__icontains=searched)
            return render(request, 'FMSApp/VDetailSearchResults.html', {'searched': searched, 'vdetails': vdetails})
        elif page == "VS":
            vspecs = InputVSpecs.objects.filter(ChassisNumber__icontains=searched) | InputVSpecs.objects.filter(
                ACUCompany__icontains=searched) | InputVSpecs.objects.filter(WheelerType__icontains=searched) | InputVSpecs.objects.filter(Engine__icontains=searched)
            return render(request, 'FMSApp/VSpecSearchResults.html', {'searched': searched, 'vspecs': vspecs})
        elif page == "DD":
            ddetails = InputDDetail.objects.filter(DriversName__icontains=searched) | InputDDetail.objects.filter(DriversAge__icontains=searched) | InputDDetail.objects.filter(
                DriversMedicalCondition__icontains=searched) | InputDDetail.objects.filter(DriversLicenseNumber__icontains=searched)
            return render(request, 'FMSApp/DDetailSearchResults.html', {'searched': searched, 'ddetails': ddetails})
    else:
        return render(request, 'FMSApp/SearchResults.html')


def FilteredSearchResults(request):
    if request.method == "POST":
        query = request.POST.getlist('selected')
        vdetails = InputVDetail.objects.filter(Q(PlateNumber__icontains=query) | Q(
            VehicleBrand__icontains=query) | Q(VehicleModel__icontains=query) | Q(GasConsumption__icontains=query))
        ddetails = InputDDetail.objects.filter(Q(DriversName__icontains=query) | Q(DriversAge__icontains=query) | Q(
            DriversMedicalCondition__icontains=query) | Q(DriversLicenseNumber__icontains=query))
        vspecs = InputVSpecs.objects.filter(Q(ChassisNumber__icontains=query) | Q(
            ACUCompany__icontains=query) | Q(WheelerType__icontains=query) | Q(Engine__icontains=query))
        return render(request, 'FMSApp/SearchResults.html', {'vdetails': vdetails, 'ddetails': ddetails, 'vspecs': vspecs})
    else:
        return render(request, 'FMSApp/SearchResults.html')


def SearchPage(request):
    return render(request, 'FMSApp/SearchPage.html')


def Vdetails(request):
    vdetails = InputVDetail.objects.all()
    return render(request, 'FMSApp/Vdetails.html', {'vdetails': vdetails})


def Vspecs(request):
    vspecs = InputVSpecs.objects.all()
    return render(request, 'FMSApp/Vspecs.html', {'vspecs': vspecs})


def Ddetails(request):
    ddetails = InputDDetail.objects.all()
    return render(request, 'FMSApp/Ddetails.html', {'ddetails': ddetails})


def Update_VDetailsPage(request, pk):
    if (request.method == "POST"):
        PNumber = request.POST.get('pN')
        VBrand = request.POST.get('vB')
        VModel = request.POST.get('vM')
        GConsumption = request.POST.get('gC')
        InputVDetail.objects.filter(pk=pk).update(
            PlateNumber=PNumber, VehicleBrand=VBrand, VehicleModel=VModel, GasConsumption=GConsumption)
        return redirect('Vdetails')
    else:
        vdetails = get_object_or_404(InputVDetail, pk=pk)
        return render(request, 'FMSApp/Update_VDetailsPage.html', {'vdetails': vdetails})


def Update_VSpecsPage(request, pk):
    if (request.method == "POST"):
        CNumber = request.POST.get('cN')
        ACompany = request.POST.get('aC')
        WType = request.POST.get('wT')
        engine = request.POST.get('eG')
        InputVSpecs.objects.filter(pk=pk).update(
            ChassisNumber=CNumber, ACUCompany=ACompany, WheelerType=WType, Engine=engine)
        return redirect('Vspecs')
    else:
        vspecs = get_object_or_404(InputVSpecs, pk=pk)
        return render(request, 'FMSApp/Update_VSpecsPage.html', {'vspecs': vspecs})


def Update_DDetailsPage(request, pk):
    if (request.method == "POST"):
        DName = request.POST.get('dN')
        DAge = request.POST.get('dA')
        DMCondition = request.POST.get('mC')
        DLNumber = request.POST.get('lN')
        InputDDetail.objects.filter(pk=pk).update(
            DriversName=DName, DriversAge=DAge, DriversMedicalCondition=DMCondition, DriversLicenseNumber=DLNumber)
        return redirect('Ddetails')
    else:
        ddetails = get_object_or_404(InputDDetail, pk=pk)
        return render(request, 'FMSApp/Update_DDetailsPage.html', {'ddetails': ddetails})


def deleteDDetailButton(request, pk):
    InputDDetail.objects.filter(pk=pk).delete()
    return redirect('Ddetails')


def MSchedPage(request, notif_id=None):
    repairs = InputMSched.objects.all()
    if notif_id is not None:
        notif = Notification.objects.filter(pk=notif_id).first()
        if notif is not None:
            notif.opened = True
            notif.save()
    return render(request, 'FMSApp/MSchedPage.html', {'repairs': repairs})


def Input_MSched(request):
    if request.method == "POST":
        input_date = request.POST.get('date')
        repair_input = request.POST['select']
        if repair_input == "customInput":
            repair_input = request.POST['customInput']
        InputMSched.objects.create(
            Date=input_date, TypeofRepairandMaintenance=repair_input)
    return render(request, 'FMSApp/Input_MSched.html')


def DeploymentPage(request):
    deployments = InputDeploymentSched.objects.all()
    return render(request, 'FMSApp/DeploymentPage.html', {'deployments': deployments})


def Input_Deployment(request):
    if request.method == 'POST':
        date_input = request.POST.get('date')
        location_input = request.POST.get('dL')
        InputDeploymentSched.objects.create(
            Date=date_input, DeploymentLocation=location_input)
    return render(request, 'FMSApp/Input_Deployment.html')


def Update_Deployment(request, pk):
    if (request.method == "POST"):
        date_input = request.POST.get('date')
        location_input = request.POST.get('dL')
        InputDeploymentSched.objects.filter(pk=pk).update(
            Date=date_input, DeploymentLocation=location_input)
        return redirect('DeploymentPage')
    else:
        deployments = get_object_or_404(InputDeploymentSched, pk=pk)
        return render(request, 'FMSApp/Update_Deployment.html', {'deployments': deployments})


def exportDeployment(request):
    deployments = InputDeploymentSched.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=deploymentsched_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Deployment Location'])
    deployments_fields = deployments.values_list('Date', 'DeploymentLocation')
    for deployment in deployments_fields:
        writer.writerow(deployment)
    return response


def Update_Maintenance(request, pk):
    maintenance = get_object_or_404(InputMSched, pk=pk)
    if request.method == "POST":
        date_input2 = request.POST.get('date')
        type_input = request.POST.get('select')
        if type_input == "Other":
            type_input = request.POST.get('customInput')
        sched = InputMSched.objects.get(pk=pk)
        if (sched is not None):
            sched.Date = date_input2
            sched.TypeofRepairandMaintenance = type_input
            sched.save()

        return redirect('MSchedPage')
    context = {
        'maintenance': maintenance,
        'maintenance_types': ["Body Paint", "Change Oil", "Add Brake Fluid"]
    }
    return render(request, 'FMSApp/Update_Maintenance.html', context)


def exportMaintenance(request):
    repairs = InputMSched.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=maintenancesched_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Maintenance and Repair Type'])
    repairs_fields = repairs.values_list('Date', 'TypeofRepairandMaintenance')
    for repair in repairs_fields:
        writer.writerow(repair)
    return response

# notif thingy

# class TaskCreateView(CreateView):
#     model = Task
#     fields = ['title', 'description', 'due_date']

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         # Create a notification for each user
#         for user in User.objects.all():
#             Notification.objects.create(task=self.object, user=user)
#         return response


def send_due_date_notifications():
    # Get all tasks due within the next day
    tomorrow = timezone.now() + timezone.timedelta(days=1)
    upcoming_tasks = Task.objects.filter(due_date__lte=tomorrow)

    # Send notifications for each task
    for task in upcoming_tasks:
        subject = f"Upcoming due date for task: {task.title}"
        message = f"Task '{task.title}' is due on {task.due_date}."
        send_mail(subject, message, 'from@example.com', [task.user.email])


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, opened=False)


class NotificationUpdateView(LoginRequiredMixin, UpdateView):
    model = Notification
    fields = ['opened']

    def get_success_url(self):
        return reverse('notification_list')
