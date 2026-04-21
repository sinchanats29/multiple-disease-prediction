from django.contrib import admin

# Register your models here.
from .models import Diabetespatientdata,parkinsonformdata,heartformdata
admin.site.register(Diabetespatientdata)
admin.site.register(heartformdata)
admin.site.register(parkinsonformdata)

