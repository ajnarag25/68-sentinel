from django.contrib import admin
from .models import User, InputVDetail, InputVSpecs, InputDDetail

# Register your models here.
admin.site.register(User)
admin.site.register(InputVDetail)
admin.site.register(InputVSpecs)
admin.site.register(InputDDetail)



