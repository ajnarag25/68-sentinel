from django.conf import settings
from datetime import datetime, timedelta, date
from FMSApp.models import InputMSched, Notification, Task


def global_context(request):
    return {
        "notif": get_notifications(),
        "unread_notif": get_unread_notifications()
    }

def get_notifications():
    one_week_from_now = datetime.today() + timedelta(days=7)
    result = Notification.objects.filter(date__lte=one_week_from_now)
    count = result.count()


    todays_schedules = InputMSched.objects.filter(Date=date.today())

    for sched in todays_schedules:        
        title = 'Maintenance Schedule (Today)'
        description = f'{sched.TypeofRepairandMaintenance}  {sched.Date}'
        existing_task = Task.objects.filter(title=title, due_date=sched.Date, description=description)
    
        if(len(existing_task) > 0):
            break
        
        task = Task.objects.create(title=title, description=description, due_date=sched.Date)
        notification = Notification.objects.create(task=task)

    return result

def get_unread_notifications():
    one_week_from_now = datetime.today() + timedelta(days=7)
    result = Notification.objects.filter(opened=False, date__lte=one_week_from_now)
    count = result.count()
    return result