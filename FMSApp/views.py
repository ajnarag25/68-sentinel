from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    InputDeploymentSched,
    User,
    InputVDetail,
    InputVSpecs,
    InputDDetail,
    InputMSched,
    DateUpdated
)
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.db.models import Q
from datetime import date
from datetime import datetime, timedelta
from django.utils import timezone
import csv

def header_data(request):
    today = timezone.now().date()

    # get the yesterday's date
    yesterday = today - timezone.timedelta(days=1)
    # calculate the date 7 days from now
    seven_days_later = today + timedelta(days=7)

    # filter the rows where status is "pending" and Date is within the range of yesterday to 7 days after
    InputMSched.objects.filter(status="pending", Date__range=[today, seven_days_later]).update(status="unread")

    # filter and update all the rows from yesterday to the past(earlier than yesterday)
    InputMSched.objects.filter(Date__lt=yesterday).update(status='read')

    # filter the rows where Date is within the range of now to 7 days after and status is "unread"
    unread_rows = InputMSched.objects.filter(Date__range=[today, seven_days_later], status="unread")
    unread_rows_count = unread_rows.count()


    # filter the rows where Date is within the range of now to 7 days after
    a_week_notif = InputMSched.objects.filter(Date__range=[today, seven_days_later]).order_by('Date')
    
        

    vehicle_model = InputVDetail.objects.values('VehicleModel').distinct()
    vehicle_brand = InputVDetail.objects.values('VehicleBrand').distinct()
    vehicle_wheeler = InputVSpecs.objects.values('WheelerType').distinct()
    vehicle_engine = InputVSpecs.objects.values('Engine').distinct()
    vehicle_repair = InputMSched.objects.values('TypeofRepairandMaintenance').distinct()
    context = {
        'now': today,
        'a_week_notif' : a_week_notif,
        'unread_rows_count' : unread_rows_count,
        'vehicle_model' : vehicle_model,
        'vehicle_brand' : vehicle_brand,
        'vehicle_wheeler' : vehicle_wheeler,
        'vehicle_engine' : vehicle_engine,
        'vehicle_repair' : vehicle_repair,

    }
    return context


def exportVDetails(request):
    vdetails = InputVDetail.objects.all()
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename=vdetails_export.csv"
    writer = csv.writer(response)
    writer.writerow(
        ["Plate Number", "Vehicle Brand", "Vehicle Model", "Gas Consumption"]
    )
    vdetails_fields = vdetails.values_list(
        "PlateNumber", "VehicleBrand", "VehicleModel", "GasConsumption"
    )
    for vdetail in vdetails_fields:
        writer.writerow(vdetail)
    return response


def exportDDetails(request):
    ddetails = InputDDetail.objects.all()
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename=ddetails_export.csv"
    writer = csv.writer(response)
    writer.writerow(
        ["Driver Name", "Driver Age", "Medical Condition", "License Number"]
    )
    ddetails_fields = ddetails.values_list(
        "DriversName", "DriversAge", "DriversMedicalCondition", "DriversLicenseNumber"
    )
    for ddetail in ddetails_fields:
        writer.writerow(ddetail)
    return response


def exportVSpecs(request):
    vspecs = InputVSpecs.objects.all()
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename=ddetails_export.csv"
    writer = csv.writer(response)
    writer.writerow(
        ["Chassis Number", "ACU Company", "Wheeler Type", "Engine", "Vehicle Image/s"]
    )
    vspecs_fields = vspecs.values_list(
        "ChassisNumber", "ACUCompany", "WheelerType", "Engine", "VehicleImage"
    )
    for vspec in vspecs_fields:
        writer.writerow(vspec)
    return response


def login(request):
    if request.method == "POST":
        u = User.objects.all()
        usernameInput = request.POST.get("uN")
        passwordInput = request.POST.get("pW")
        if (u.filter(username=usernameInput)) and (u.filter(password=passwordInput)):
            usr = get_object_or_404(
                User, username=usernameInput, password=passwordInput
            )
            request.session["user"] = usr.username
            request.session["userPK"] = usr.pk
            return redirect("main_menu")
        else:
            return render(
                request,
                "FMSApp/login.html",
                {"invalidLogin": "Incorrect Username or Password"},
            )
    else:
        return render(request, "FMSApp/login.html")


def main_menu(request):
    ddetails = InputVSpecs.objects.select_related("PlateNumber").all()
    ddriver = InputDDetail.objects.select_related("PlateNumber").all()
    msched = InputMSched.objects.select_related("PlateNumber").all()
    deployment = InputDeploymentSched.objects.select_related("PlateNumber").all()

    context = {
        "ddetails": ddetails,
        "ddriver": ddriver,
        "msched": msched,
        "deploy": deployment,
    }
    return render(request, "FMSApp/main_menu.html", context)


def logout(request):
    del request.session["user"]
    return render(request, "FMSApp/login.html")


def Input_VDetails(request):
    d = InputVDetail.objects.all()
    if request.method == "POST":
        PlateNumberInput = request.POST.get("pN")
        VehicleBrandInput = request.POST.get("vB")
        VehicleModelInput = request.POST.get("vM")
        GasConsumptionInput = request.POST.get("gC")
        InputVDetail.objects.create(
            PlateNumber=PlateNumberInput,
            VehicleBrand=VehicleBrandInput,
            VehicleModel=VehicleModelInput,
            GasConsumption=GasConsumptionInput,
        )
        get_id= InputVDetail.objects.filter(PlateNumber=PlateNumberInput).values_list('id', flat=True)
        fetch_id = None
        for gett in get_id:
            fetch_id = gett
        print(fetch_id)
        
        obj, created = DateUpdated.objects.get_or_create(platenumber_id=fetch_id)
        if not created:
            obj.date_updated = date.today()
            obj.save()
    return render(request, "FMSApp/Input_VDetails.html")


from django.contrib import messages


def Input_VSpecs(request):
    # Get all vehicle details
    get_Vdetails = InputVDetail.objects.values()

    if request.method == "POST":
        PlateNumberInput = request.POST.get("pN")
        ChassisNumberInput = request.POST.get("cN")
        ACUCompanyInput = request.POST.get("aC")
        WheelerTypeInput = request.POST.get("wT")
        EngineInput = request.POST.get("eG")
        upload = request.FILES["upload"]
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)

        # Check if the input vehicle specs already exist
        existing_input = InputVSpecs.objects.filter(
            PlateNumber_id=PlateNumberInput
        ).exists()

        if existing_input:
            error_message = "Input vehicle specifications already exists"
            print(error_message)
            return render(
                request,
                "FMSApp/Input_VSpecs.html",
                {
                    "file_url": file_url,
                    "plate_numbers": get_Vdetails,
                    "error_message": error_message,
                },
            )
        else:
            # Create a new input vehicle specs object
            InputVSpecs.objects.create(
                PlateNumber_id=PlateNumberInput,
                ChassisNumber=ChassisNumberInput,
                ACUCompany=ACUCompanyInput,
                WheelerType=WheelerTypeInput,
                Engine=EngineInput,
                VehicleImage=upload,
            )
            print(PlateNumberInput)
            obj, created = DateUpdated.objects.get_or_create(platenumber_id=PlateNumberInput)
            if not created:
                obj.date_updated = date.today()
                obj.save()

        # Remove the selected option from the dropdown menu
        get_Vdetails = InputVDetail.objects.exclude(id=PlateNumberInput).values()

        return render(
            request,
            "FMSApp/Input_VSpecs.html",
            {
                "file_url": file_url,
                "plate_numbers": get_Vdetails,
            },
        )

    # Render the form with all vehicle details
    context = {"plate_numbers": get_Vdetails}
    return render(request, "FMSApp/Input_VSpecs.html", context)


def Input_DDetails(request):
    get_Vdetails = InputVDetail.objects.values()

    if request.method == "POST":
        PlateNumberInput = request.POST.get("pN")
        DriverNameInput = request.POST.get("dN")
        DriverAgeInput = request.POST.get("dA")
        MedicalConditionInput = request.POST.get("mC")
        LicenseNumberInput = request.POST.get("lN")

        # Check if the input driver details already exist for the given plate number
        existing_input = InputDDetail.objects.filter(
            PlateNumber_id=PlateNumberInput
        ).exists()

        if existing_input:
            error_message = (
                "Input driver details already exist for the selected vehicle"
            )
            print(error_message)
            return render(
                request,
                "FMSApp/Input_DDetails.html",
                {
                    "plate_numbers": get_Vdetails,
                    "error_message": error_message,
                },
            )
        else:
            # Create a new input driver details object
            InputDDetail.objects.create(
                PlateNumber_id=PlateNumberInput,
                DriversName=DriverNameInput,
                DriversAge=DriverAgeInput,
                DriversMedicalCondition=MedicalConditionInput,
                DriversLicenseNumber=LicenseNumberInput,
            )
            print(PlateNumberInput)
            obj, created = DateUpdated.objects.get_or_create(platenumber_id=PlateNumberInput)
            if not created:
                obj.date_updated = date.today()
                obj.save()
            
        # Remove the selected option from the dropdown menu
        get_Vdetails = InputVDetail.objects.exclude(id=PlateNumberInput).values()

        return render(
            request,
            "FMSApp/Input_DDetails.html",
            {
                "plate_numbers": get_Vdetails,
            },
        )

    # Render the form with all vehicle details
    context = {"plate_numbers": get_Vdetails}
    return render(request, "FMSApp/Input_DDetails.html", context)


def SearchResults(request):
    if request.method == "POST":
        page = request.POST.get("page")
        searched = request.POST["searched"]
        if page == "A":
            vdetails = (
                InputVDetail.objects.filter(PlateNumber__icontains=searched)
                | InputVDetail.objects.filter(VehicleBrand__icontains=searched)
                | InputVDetail.objects.filter(VehicleModel__icontains=searched)
                | InputVDetail.objects.filter(GasConsumption__icontains=searched)
            )
            ddetails = (
                InputDDetail.objects.filter(DriversName__icontains=searched)
                | InputDDetail.objects.filter(DriversAge__icontains=searched)
                | InputDDetail.objects.filter(
                    DriversMedicalCondition__icontains=searched
                )
                | InputDDetail.objects.filter(DriversLicenseNumber__icontains=searched)
            )
            vspecs = (
                InputVSpecs.objects.filter(ChassisNumber__icontains=searched)
                | InputVSpecs.objects.filter(ACUCompany__icontains=searched)
                | InputVSpecs.objects.filter(WheelerType__icontains=searched)
                | InputVSpecs.objects.filter(Engine__icontains=searched)
            )
            return render(
                request,
                "FMSApp/SearchResults.html",
                {
                    "searched": searched,
                    "vdetails": vdetails,
                    "ddetails": ddetails,
                    "vspecs": vspecs,
                },
            )
        elif page == "VD":
            vdetails = (
                InputVDetail.objects.filter(PlateNumber__icontains=searched)
                | InputVDetail.objects.filter(VehicleBrand__icontains=searched)
                | InputVDetail.objects.filter(VehicleModel__icontains=searched)
                | InputVDetail.objects.filter(GasConsumption__icontains=searched)
            )
            return render(
                request,
                "FMSApp/VDetailSearchResults.html",
                {"searched": searched, "vdetails": vdetails},
            )
        elif page == "VS":
            vspecs = (
                InputVSpecs.objects.filter(ChassisNumber__icontains=searched)
                | InputVSpecs.objects.filter(ACUCompany__icontains=searched)
                | InputVSpecs.objects.filter(WheelerType__icontains=searched)
                | InputVSpecs.objects.filter(Engine__icontains=searched)
            )
            return render(
                request,
                "FMSApp/VSpecSearchResults.html",
                {"searched": searched, "vspecs": vspecs},
            )
        elif page == "DD":
            ddetails = (
                InputDDetail.objects.filter(DriversName__icontains=searched)
                | InputDDetail.objects.filter(DriversAge__icontains=searched)
                | InputDDetail.objects.filter(
                    DriversMedicalCondition__icontains=searched
                )
                | InputDDetail.objects.filter(DriversLicenseNumber__icontains=searched)
            )
            return render(
                request,
                "FMSApp/DDetailSearchResults.html",
                {"searched": searched, "ddetails": ddetails},
            )
    else:
        return render(request, "FMSApp/SearchResults.html")


def FilteredSearchResults(request):
    if request.method == "POST":
        date_updated_list = []
        vmodel_list = []
        vbrand_list = []
        vwheeler_list = []
        vengine_list = []
        vrepair_list = []
        get_common_indices = []

        date_updated = request.POST.get("date_updated")
        
        vmodel = request.POST.getlist("vmodel")

        
        vbrand = request.POST.getlist("vbrand")

        
        vwheeler = request.POST.getlist("vwheeler")

        
        vengine = request.POST.getlist("vengine")


        vrepair = request.POST.getlist("vrepair")

        
    

        now = datetime.now()
        #declaring the dates 1 week, one day, and 1 month ago

        last_24_hours = now - timedelta(hours=24)
        last_24_hours = timezone.make_aware(last_24_hours)
        
        one_week_ago = now - timedelta(days=7)
        one_week_ago = timezone.make_aware(one_week_ago)


        one_month_ago = timezone.now() - timedelta(days=30)
        
        #if condition for the date update

        if(date_updated == 'oneday'):
            # fetch_id_date = DateUpdated.objects.filter(date_updated__gte=last_24_hours).values_list('PlateNumber_id', flat=True).distinct()
            fetch_id_date = DateUpdated.objects.filter(date_updated__range=[last_24_hours, now]).distinct()
            for obj in fetch_id_date:
                date_updated_list.append(obj.platenumber_id)
            print(date_updated_list)

        elif(date_updated == 'thisweek'):
            # fetch_id_date = DateUpdated.objects.filter(date_updated__gte=one_week_ago).values_list('PlateNumber_id', flat=True).distinct()
            fetch_id_date = DateUpdated.objects.filter(date_updated__range=[one_week_ago, now]).distinct()
            for obj in fetch_id_date:
                date_updated_list.append(obj.platenumber_id)
            print(date_updated_list)

        elif(date_updated == 'thismonth'):
            fetch_id_date = DateUpdated.objects.filter(date_updated__range=[one_month_ago, now]).distinct()
            for obj in fetch_id_date:
                date_updated_list.append(obj.platenumber_id)
            print(date_updated_list)
        
        else:
            for obj in DateUpdated.objects.all():
                date_updated_list.append(obj.platenumber_id)
            print(date_updated_list)
        
        



        #if condition for the vehicle model
        if(len(vmodel) == 0 or vmodel[0] == "all"):
            for obj in InputVDetail.objects.all():
                vmodel_list.append(obj.id)
            print(vmodel_list)
        else:
            
            vmodels = InputVDetail.objects.filter(VehicleModel__in=vmodel)
            vmodel_list = [vmodel.id for vmodel in vmodels]
            print(vmodel_list)




        #if condition in vehicle brand

        if(len(vbrand) == 0 or vbrand[0] == "all"):
            for obj in InputVDetail.objects.all():
                vbrand_list.append(obj.id)
            print(vbrand_list)
        else:
           
            vbrands = InputVDetail.objects.filter(VehicleBrand__in=vbrand)
            vbrand_list = [vbrand.id for vbrand in vbrands]
            print(vbrand_list)


        # if condition for wheeler type

        if(len(vwheeler) == 0 or vwheeler[0] == "all"):
            for obj in InputVSpecs.objects.all():
                vwheeler_list.append(obj.PlateNumber_id)
            print(vbrand_list)
        else:
           
            vwheelers = InputVSpecs.objects.filter(WheelerType__in=vwheeler)
            vwheeler_list = [vwheeler.PlateNumber_id for vwheeler in vwheelers]
            print(vwheeler_list)

        
        # if condition for engine type
        if(len(vengine) == 0 or vengine[0] == "all"):
            for obj in InputVSpecs.objects.all():
                vengine_list.append(obj.PlateNumber_id)
            print(vengine_list)
        else:
           
            vengines = InputVSpecs.objects.filter(Engine__in=vengine)
            vengine_list = [vengine.PlateNumber_id for vengine in vengines]
            print(vengine_list)
        

        # if condition for repair
        if(len(vrepair) == 0 or vrepair[0] == "all"):
            vrepairs = InputMSched.objects.values_list('PlateNumber_id', flat=True).distinct()
            for vrepair in vrepairs:
                vrepair_list.append(vrepair)
            print(vrepair_list)
        else:
            vrepairs =InputMSched.objects.filter(TypeofRepairandMaintenance__in=vrepair).values_list('PlateNumber_id', flat=True).distinct()
            for vrepair in vrepairs:
                vrepair_list.append(vrepair)
            print(vrepair_list)

        #this code is to collect all common plate number ids per lists

        for get_common in date_updated_list:
            if get_common in vmodel_list and get_common in vbrand_list and get_common in vwheeler_list and get_common in vengine_list and get_common in vrepair_list:
                get_common_indices.append(get_common)
        print(get_common_indices)
        

        #IN THIS SECTION, WE WILL SEND THE COMMON INDICES TO THE TABLE TO DISPLAY THE DATA INSIDE THE HTML TABLE
        vdetails = InputVDetail.objects.filter(id__in=get_common_indices) 
        data = []
        for vdetail in vdetails:
            vspecs = InputVSpecs.objects.filter(PlateNumber_id=vdetail.id)
            ddetails = InputDDetail.objects.filter(PlateNumber_id=vdetail.id)
            data.append({'platenumber':vdetail.PlateNumber , 'vbrand': vdetail.VehicleBrand , 'vmodel':vdetail.VehicleModel ,'gas':vdetail.GasConsumption, 'vspecs_data':vspecs , 'ddetails_data':ddetails})
            print(ddetails)
        print(data)
        return render(request,"FMSApp/SearchResults.html",{'data': data})
    else:
        return render(request, "FMSApp/SearchResults.html")


def SearchPage(request):
    return render(request, "FMSApp/SearchPage.html")


def Vdetails(request):
    vdetails = InputVDetail.objects.all()
    return render(request, "FMSApp/Vdetails.html", {"vdetails": vdetails})


def Vspecs(request):
    vspecs = InputVSpecs.objects.all()
    return render(request, "FMSApp/Vspecs.html", {"vspecs": vspecs})


def Ddetails(request):
    ddetails = InputDDetail.objects.all()
    return render(request, "FMSApp/Ddetails.html", {"ddetails": ddetails})


def Update_VDetailsPage(request, pk):
    if request.method == "POST":
        PNumber = request.POST.get("pN")
        VBrand = request.POST.get("vB")
        VModel = request.POST.get("vM")
        GConsumption = request.POST.get("gC")
        InputVDetail.objects.filter(pk=pk).update(
            PlateNumber=PNumber,
            VehicleBrand=VBrand,
            VehicleModel=VModel,
            GasConsumption=GConsumption,
        )
        return redirect("Vdetails")
    else:
        vdetails = get_object_or_404(InputVDetail, pk=pk)
        return render(
            request, "FMSApp/Update_VDetailsPage.html", {"vdetails": vdetails}
        )


def Update_VSpecsPage(request, pk):
    if request.method == "POST":
        CNumber = request.POST.get("cN")
        ACompany = request.POST.get("aC")
        WType = request.POST.get("wT")
        engine = request.POST.get("eG")
        InputVSpecs.objects.filter(pk=pk).update(
            ChassisNumber=CNumber, ACUCompany=ACompany, WheelerType=WType, Engine=engine
        )
        return redirect("Vspecs")
    else:
        vspecs = get_object_or_404(InputVSpecs, pk=pk)
        return render(request, "FMSApp/Update_VSpecsPage.html", {"vspecs": vspecs})


def Update_DDetailsPage(request, pk):
    if request.method == "POST":
        DName = request.POST.get("dN")
        DAge = request.POST.get("dA")
        DMCondition = request.POST.get("mC")
        DLNumber = request.POST.get("lN")
        InputDDetail.objects.filter(pk=pk).update(
            DriversName=DName,
            DriversAge=DAge,
            DriversMedicalCondition=DMCondition,
            DriversLicenseNumber=DLNumber,
        )
        return redirect("Ddetails")
    else:
        ddetails = get_object_or_404(InputDDetail, pk=pk)
        return render(
            request, "FMSApp/Update_DDetailsPage.html", {"ddetails": ddetails}
        )


def deleteDDetailButton(request, pk):
    InputDDetail.objects.filter(pk=pk).delete()
    return redirect("Ddetails")


def MSchedPage(request,id):
    print(id)
    InputMSched.objects.filter(id=id).update(status="read")
    msched_list = InputMSched.objects.order_by('-Date').all()
    datas = {
        'msched_list': msched_list
    }
    return render(request, "FMSApp/MSchedPage.html", datas)


from .models import InputMSched


def Input_MSched(request):
    get_Vdetails = InputVDetail.objects.values()
    # Check if the input driver details already exist for the given plate number
    if request.method == "POST":
        PlateNumberInput = request.POST.get("pN")
        input_date = request.POST.get("date")
        repair_input = request.POST["select"]
        existing_input = InputMSched.objects.filter(
            PlateNumber_id=PlateNumberInput
        ).exists()

        if existing_input:
            error_message = (
                "Input maintenance schedule already exists for the selected vehicle"
            )
            print(error_message)
            return render(
                request,
                "FMSApp/Input_MSched.html",
                {
                    "plate_numbers": get_Vdetails,
                    "error_message": error_message,
                },
            )
        else:
            # Create a new input maintenance schedule object
            InputMSched.objects.create(
                PlateNumber_id=PlateNumberInput,
                Date=input_date,
                TypeofRepairandMaintenance=repair_input,
            )
            print(PlateNumberInput)
            obj, created = DateUpdated.objects.get_or_create(platenumber_id=PlateNumberInput)
            if not created:
                obj.date_updated = date.today()
                obj.save()
            # Remove the selected option from the dropdown menu
            get_Vdetails = InputVDetail.objects.exclude(id=PlateNumberInput).values()
            return render(
                request,
                "FMSApp/Input_MSched.html",
                {
                    "plate_numbers": get_Vdetails,
                },
            )

    # Remove the selected option from the dropdown menu
    PlateNumberInput = None
    get_Vdetails = InputVDetail.objects.values()
    context = {"plate_numbers": get_Vdetails}
    return render(request, "FMSApp/Input_MSched.html", context)


def DeploymentPage(request):
    deployments = InputDeploymentSched.objects.all()
    return render(request, "FMSApp/DeploymentPage.html", {"deployments": deployments})


def Input_Deployment(request):
    get_Vdetails = InputVDetail.objects.values()
    # Check if the input driver details already exist for the given plate number
    if request.method == "POST":
        PlateNumberInput = request.POST.get("pN")
        date_input = request.POST.get("date")
        location_input = request.POST.get("dL")
        existing_input = InputDeploymentSched.objects.filter(
            PlateNumber_id=PlateNumberInput
        ).exists()

        if existing_input:
            error_message = "Input deployment already exists for the selected vehicle"
            print(error_message)
            return render(
                request,
                "FMSApp/Input_Deployment.html",
                {
                    "plate_numbers": get_Vdetails,
                    "error_message": error_message,
                },
            )
        else:
            # Create a new input maintenance schedule object
            InputDeploymentSched.objects.create(
                PlateNumber_id=PlateNumberInput,
                Date=date_input,
                DeploymentLocation=location_input,
            )
            print(PlateNumberInput)
            obj, created = DateUpdated.objects.get_or_create(platenumber_id=PlateNumberInput)
            if not created:
                obj.date_updated = date.today()
                obj.save()
            # Remove the selected option from the dropdown menu
            get_Vdetails = InputVDetail.objects.exclude(id=PlateNumberInput).values()
            return render(
                request,
                "FMSApp/Input_Deployment.html",
                {
                    "plate_numbers": get_Vdetails,
                },
            )

    # Remove the selected option from the dropdown menu
    PlateNumberInput = None
    get_Vdetails = InputVDetail.objects.values()
    context = {"plate_numbers": get_Vdetails}
    return render(request, "FMSApp/Input_Deployment.html", context)


def Update_Deployment(request, pk):
    if(request.method=="POST"):
        date_input = request.POST.get('date')
        location_input = request.POST.get('dL')
        InputDeploymentSched.objects.filter(pk=pk).update(Date=date_input, DeploymentLocation=location_input)
        return redirect('DeploymentPage')
    else:
        deployments = get_object_or_404(InputDeploymentSched, pk=pk)
        return render(request, 'FMSApp/Update_Deployment.html', {'deployments': deployments})
        


def exportDeployment(request):
    deployments = InputDeploymentSched.objects.all()
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename=deploymentsched_export.csv"
    writer = csv.writer(response)
    writer.writerow(["Date", "Deployment Location"])
    deployments_fields = deployments.values_list("Date", "DeploymentLocation")
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
        if(sched is not None):
            sched.Date=date_input2
            sched.TypeofRepairandMaintenance=type_input
            sched.save()
            date_input2_obj = datetime.strptime(date_input2, '%Y-%m-%d')
            today = datetime.today().date()
            date_diff = (date_input2_obj.date() - today).days
            if date_diff >= 0 and date_diff <= 7:
                InputMSched.objects.filter(id=pk).update(status='unread')
            else:
                pass

        return redirect('MSchedPage')
    context = {
        'maintenance': maintenance,
        'maintenance_types': ["Body Paint", "Change Oil", "Add Brake Fluid"]
    }
    return render(request, 'FMSApp/Update_Maintenance.html', context)



def exportMaintenance(request):
    repairs = InputMSched.objects.all()
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename=maintenancesched_export.csv"
    writer = csv.writer(response)
    writer.writerow(["Date", "Maintenance and Repair Type"])
    repairs_fields = repairs.values_list("Date", "TypeofRepairandMaintenance")
    for repair in repairs_fields:
        writer.writerow(repair)
    return response
