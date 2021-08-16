from django.contrib import admin
# from .models import User
from .models import Employee, Patient, Appointment
# Register your models here.

# admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Patient)
admin.site.register(Appointment)