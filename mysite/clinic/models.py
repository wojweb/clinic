from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

# Create your models here.

class Employee(models.Model):
    
    class Position(models.TextChoices):
        DOCTOR = 'doctor'
        RECEPTIONIST = 'receptionist'

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    privilege = models.CharField(max_length = 50, choices = Position.choices)

    name = models.CharField(max_length = 64)
    last_name = models.CharField(max_length = 64)
    adress = models.CharField(max_length = 100, blank = True)
    phone_number = models.CharField(max_length = 64, blank = True)
    salary = models.IntegerField(default = 0, blank = True)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Patient(models.Model):
    pesel = models.CharField(max_length = 11, primary_key=True)
    name = models.CharField(max_length = 64)
    last_name = models.CharField(max_length = 64)
    adress = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 64)

    def __str__(self):
        return f'{self.name}'

class Treatment(models.Model):
    name = models.CharField(max_length = 100, primary_key=True)
    informations = models.CharField(max_length = 200)
    price = models.IntegerField(default=0)
    refundable = models.BooleanField()

    def __str__(self):
        return f'{self.name}'

class Appointment(models.Model):

    POSSIBLE_TIMES = [
        ('8', '8.00'),
        ('83', '8.30'),
        ('9', '9.00'),
        ('93', '9.30'),
        ('10', '10.00'),
        ('1030', '10.30'),
        ('11', '11.00'),
        ('113', '11.30'),
        ('12', '12.00'),
        ('123', '12.30'),
        ('13', '13.00'),
        ('133', '13.30')
    ]

    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    doctor = models.ForeignKey(Employee, on_delete = models.CASCADE)
    date = models.DateField()
    time = models.TextField(choices= POSSIBLE_TIMES)
    treatment = models.ForeignKey(Treatment, on_delete = models.CASCADE)
    results = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.patient} - {self.treatment}: {self.date}   {self.time}'



    

