from django.contrib import admin
from .models import Doctors, Patients, CustomUser


admin.site.register(Doctors)
admin.site.register(Patients)
admin.site.register(CustomUser)
