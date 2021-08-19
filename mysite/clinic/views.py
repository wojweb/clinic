from django.shortcuts import render, reverse
from django.http import (HttpResponse, HttpResponseRedirect, HttpResponseNotFound,
    HttpResponseBadRequest)
from django.views import generic
from .models import Employee, Treatment, Patient, Appointment
from .forms import (LoginForm, NewEmployeeForm, EmployeeReadOnlyForm,
    EmployeeForm, ChangePasswordForm, NewTreatmentForm, TreatmentForm, TreatmentReadOnlyForm,
    FindPatientForm, NewPatientForm, PatientReadOnlyForm, PatientForm, NewAppointmentForm, 
    NewAppointmentFormTime, AppointmentReadOnlyForm)
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
import sys
from django.http import Http404


logger  = logging.getLogger(__name__)
# Create your views here.

class WrongPassword(Exception):
    pass

not_found_html = """
            <!doctype html>
            <html lang="en">
            <head>
                <title>Not Found</title>
            </head>
            <body>
                <h1>Not Found</h1><p>The requested resource was not found on this server.</p>
            </body>
            </html>"""

bed_request_html = """
            <!doctype html>
            <html lang="en">
            <head>
                <title>Not Found</title>
            </head>
            <body>
                <h1>Not Found</h1><p>WARNING!!! Something went wrong.</p>
            </body>
            </html>"""

def index(request):
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if(form.is_valid()):
            try:
                user = authenticate(request, username = form.cleaned_data['login'],
                    password=form.cleaned_data['password'])
                
                if user is not None:
                    login(request, user)
                    if user.is_superuser:
                        return HttpResponseRedirect(reverse('clinic:admin'))
                    else:
                        employee = Employee.objects.get(user=user)
                        if employee.privilege == Employee.Position.DOCTOR:
                            return HttpResponseRedirect(reverse('clinic:doctor',
                                args=(user.username,)))
                        else:
                            return HttpResponseRedirect(reverse('clinic:receptionist'))
                else:
                    raise WrongPassword

            except(KeyError, WrongPassword):
                return render(request, 'clinic/index.html', {
                    'form': form,
                    'message': "Uncorrect login or password"
                })
            except(Employee.DoesNotExist):
                return render(request, 'clinic/index.html', {
                    'form': form,
                    'message': "I can't find this specific employee"
                })

    else:
        form = LoginForm()
    return render(request, 'clinic/index.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('clinic:index'))

def test(request):
    return render(request, 'clinic/test.html', {})

def temp(request):
    return render(request, 'clinic/temp.html', {})

def admin_employee_details(request, login):
    if not request.user.is_superuser:
        return HttpResponseNotFound(not_found_html)

    user = User.objects.get(username=login)
    employee = Employee.objects.get(user=user)
    def helper(x):
        if x == Employee.Position.DOCTOR:
            return 'Doctor'
        else:
            return 'Receptionist'
    
    form = EmployeeReadOnlyForm(initial={'login':employee.user.username,
                            'name':employee.name,
                            'lastname':employee.last_name,
                            'position':helper(employee.privilege),
                            'address':employee.adress,
                            'phone':employee.phone_number,
                            'salary':employee.salary
                            })

    return render(request, 'clinic/admin_employee_details.html', {'form': form, 'login1':login})

def admin_employee_update(request, login):
    if not request.user.is_superuser:
        return HttpResponseNotFound(not_found_html)

    if request.method == 'POST':

        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username = form.cleaned_data['login'])
            employee = Employee.objects.get(user=user)
            employee.name = form.cleaned_data['name']
            employee.last_name = form.cleaned_data['lastname']
            if form.cleaned_data['position'] == 'doctor':
                employee.privilege = Employee.Position.DOCTOR
            else:
                employee.privilege = Employee.Position.RECEPTIONIST
            employee.adress = form.cleaned_data['address']
            employee.phone_number = form.cleaned_data['phone']
            employee.salary = form.cleaned_data['salary']
            employee.save()
            return HttpResponseRedirect(reverse('clinic:employee_details', args=(form.cleaned_data['login'],)))
        else:
            raise Exception

    else:
        user = User.objects.get(username=login)
        employee = Employee.objects.get(user=user)
        form = EmployeeForm(initial={'login':user.username,
                            'name':employee.name,
                            'lastname':employee.last_name,
                            'position':employee.privilege,
                            'address':employee.adress,
                            'phone':employee.phone_number,
                            'salary':employee.salary
                            })

    return render(request, 'clinic/admin_employee_update.html', {'form': form, 'login1':login})

def admin_employee_remove(request, login):
    if not request.user.is_superuser:
        return HttpResponseNotFound(not_found_html)

    user = User.objects.get(username=login)
    employee = Employee.objects.get(user=user)
    employee.delete()
    user.delete()
    return HttpResponseRedirect(reverse('clinic:admin'))

def admin_change_password(request, login):
    if not request.user.is_superuser:
        return HttpResponseNotFound(not_found_html)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
                try:
                    if form.cleaned_data['password'] != form.cleaned_data['repeat_password']:
                        raise WrongPassword
                    user = User.objects.get(username = login)
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    return HttpResponseRedirect(reverse('clinic:employee_details', args=(login,)))


                except WrongPassword:
                    form = ChangePasswordForm()
                    return render(request, 'clinic/admin_change_password.html', {'form':form, 'login1': login,
                        'password_message':'Passwords must be the same'})




    else:
        form = ChangePasswordForm()
        return render(request, 'clinic/admin_change_password.html', {'form':form, 'login1': login})

def admin_new_employee(request):
    if not request.user.is_superuser:
        return HttpResponseNotFound(not_found_html)

    if request.method == 'POST':
        form = NewEmployeeForm(request.POST)

        if form.is_valid():
            try:
                if form.cleaned_data['password'] != form.cleaned_data['repeat_password']:
                    raise WrongPassword

                user = User.objects.get(username = form.cleaned_data['login'])
                employee = Employee.objects.get(user=user)
                return render(request, 'clinic/admin_new_employee.html', {'form':form, 'login_message':"This login is busy"})

                
            except User.DoesNotExist:

                user = User.objects.create_user(form.cleaned_data['login'], password=form.cleaned_data['password'])
                user.save()
                employee = Employee(user = user,
                                name=form.cleaned_data['name'],
                                last_name=form.cleaned_data['lastname'],
                                privilege=form.cleaned_data['position'],
                                adress=form.cleaned_data['address'],
                                phone_number=form.cleaned_data['phone'],
                                salary=form.cleaned_data['salary']
                )
                employee.save()
                return HttpResponseRedirect(reverse('clinic:admin'))

            except WrongPassword:
                return render(request, 'clinic/admin_new_employee.html', {'form':form, 'password_message':"Passwords must be the same"})

    else:
        form = NewEmployeeForm()
    
    return render(request, 'clinic/admin_new_employee.html', {'form':form})

def admin_new_treatment(request):
    if not request.user.is_superuser:
        return HttpResponseNotFound(not_found_html)
    if request.method == 'POST':
        form = NewTreatmentForm(request.POST)

        if form.is_valid():
            try:

                user = Treatment.objects.get(name = form.cleaned_data['name'])
                return render(request, 'clinic/admin_new_treatment.html', {'form':form, 'name_message':"This name is busy"})

                
            except Treatment.DoesNotExist:

                treatment = Treatment(name=form.cleaned_data['name'],
                                informations=form.cleaned_data['informations'],
                                price=form.cleaned_data['price'],
                                refundable=form.cleaned_data['refundable'],
                )
                treatment.save()
                return HttpResponseRedirect(reverse('clinic:treatments'))


    else:
        form = NewTreatmentForm()
    
    return render(request, 'clinic/admin_new_treatment.html', {'form':form})

def admin_treatment_details(request, name):
    if not request.user.is_superuser:
        return HttpResponseNotFound(not_found_html)

    treatment = Treatment.objects.get(name=name)

    form = TreatmentReadOnlyForm(initial={'name': treatment.name,
                            'informations': treatment.informations,
                            'price': treatment.price,
                            'refundable': treatment.refundable,
                            })

    return render(request, 'clinic/admin_treatment_details.html', {'form': form, 'name':name})

def admin_treatment_update(request, name):
    if not request.user.is_superuser:
        return HttpResponseNotFound(not_found_html)
    
    if request.method == 'POST':

        form = TreatmentForm(request.POST)
        if form.is_valid():
            treatment = Treatment.objects.get(name = name)
            treatment.name = form.cleaned_data['name']
            treatment.informations = form.cleaned_data['informations']
            treatment.price = form.cleaned_data['price']
            treatment.refundable = form.cleaned_data['refundable']
            treatment.save()
            return HttpResponseRedirect(reverse('clinic:treatment_details', args=(form.cleaned_data['name'],)))
        else:
            raise Exception

    else:
        treatment = Treatment.objects.get(name=name)
        form = TreatmentForm(initial={'name':treatment.name,
                            'informations':treatment.informations,
                            'price':treatment.price,
                            'refundable':treatment.refundable,
                            })

    return render(request, 'clinic/admin_treatment_update.html', {'form': form, 'name': name})

def admin_treatment_remove(request, name):
    if not request.user.is_superuser:
        return HttpResponseNotFound(not_found_html)

    treatment = Treatment.objects.get(name=name)
    treatment.delete()

    return HttpResponseRedirect(reverse('clinic:treatments'))

class AdminListView(UserPassesTestMixin, generic.ListView):
    model = Employee
    template_name = 'clinic/admin.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context =  super().get_context_data(object_list=object_list, **kwargs)
        context['enumerated_object_list'] = [(i + 1, k) for i, k in enumerate(context['object_list'])]

        return context

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseNotFound(not_found_html)

class TreatmentsListView(UserPassesTestMixin, generic.ListView):
    model = Treatment
    template_name = 'clinic/admin_treatments.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context =  super().get_context_data(object_list=object_list, **kwargs)
        context['enumerated_object_list'] = [(i + 1, k) for i, k in enumerate(context['object_list'])]
        return context

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseNotFound(not_found_html)

class DoctorView(generic.DetailView):
    model = Employee
    template_name = 'clinic/doctor.html'

def receptionist(request):
    if not request.user.is_authenticated or \
        not Employee.objects.get(user = request.user).privilege == Employee.Position.RECEPTIONIST:
        return HttpResponseNotFound(not_found_html)


    if request.method == 'POST':
        form = FindPatientForm(request.POST)
        if(form.is_valid()):
            try:
                patient = Patient.objects.get(pesel = form.cleaned_data['pesel'])
                return HttpResponseRedirect(reverse('clinic:patient',
                    args=(patient.pesel,)))

            except(Patient.DoesNotExist):
                return render(request, 'clinic/receptionist.html', {
                'form': form,
                'message': "We have no patient with a given PESEL"
            })
    else:
        form = FindPatientForm()

    return render(request, 'clinic/receptionist.html', {'form': form})

def receptionist_new_patient(request):
    if not request.user.is_authenticated or \
        not Employee.objects.get(user = request.user).privilege == Employee.Position.RECEPTIONIST:
        return HttpResponseNotFound(not_found_html)

    if request.method == 'POST':
        form = NewPatientForm(request.POST)

        if form.is_valid():
            try:
                patient = Patient.objects.get(pesel = form['pesel'])
                return render(request, 'clinic/receptionist_new_patient.html', {'form':form, 'pesel_message':"Patient with a given PESEL already is in the database"})

            except:
                patient = Patient(pesel = form.cleaned_data['pesel'],
                                name=form.cleaned_data['name'],
                                last_name=form.cleaned_data['lastname'],
                                adress=form.cleaned_data['address'],
                                phone_number=form.cleaned_data['phone_number'],
                )
                patient.save()
                return HttpResponseRedirect(reverse('clinic:patient', args=(form.cleaned_data['pesel'],)))
    
    form = NewPatientForm()

    return render(request, 'clinic/receptionist_new_patient.html', {'form':form})

def receptionist_patient(request, pesel):
    if not request.user.is_authenticated or \
        not Employee.objects.get(user = request.user).privilege == Employee.Position.RECEPTIONIST:
        return HttpResponseNotFound(not_found_html)
    
    patient = Patient.objects.get(pesel = pesel)

    form = PatientReadOnlyForm(initial={'pesel':pesel, 'name':patient.name,
                                'lastname':patient.last_name, 'address': patient.adress,
                                'phone_number':patient.phone_number})

    incoming_appointments = list(Appointment.objects.all().filter(results = '')
        .filter(patient = patient))
    past_appointments = list(Appointment.objects.all().exclude(results = '')
        .filter(patient = patient))
    return render(request, 'clinic/receptionist_patient.html', {'form':form, 'pesel':pesel,
        'incoming_appointments':incoming_appointments, 'past_appointments':past_appointments})

def receptionist_patient_update(request, pesel):
    if not request.user.is_authenticated or \
        not Employee.objects.get(user = request.user).privilege == Employee.Position.RECEPTIONIST:
        return HttpResponseNotFound(not_found_html)
    

    if request.method == 'POST':

        form = PatientForm(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(pesel = pesel)
            patient.name = form.cleaned_data['name']
            patient.last_name = form.cleaned_data['lastname']
            patient.adress = form.cleaned_data['address']
            patient.phone_number = form.cleaned_data['phone_number']
            patient.save()
            return HttpResponseRedirect(reverse('clinic:patient', args=(form.cleaned_data['pesel'],)))
        else:
            raise Exception

    else:

        patient = Patient.objects.get(pesel = pesel)
    
        form = PatientForm(initial={'pesel':pesel, 'name':patient.name,
                                'lastname':patient.last_name, 'address': patient.adress,
                                'phone_number':patient.phone_number})

    return render(request, 'clinic/receptionist_patient_update.html', {'form':form, 'pesel': pesel})

def receptionist_patient_remove(request, pesel):
    if not request.user.is_authenticated or \
        not Employee.objects.get(user = request.user).privilege == Employee.Position.RECEPTIONIST:
        return HttpResponseNotFound(not_found_html)
    
    patient = Patient.objects.get(pesel = pesel)
    patient.delete()
    return HttpResponseRedirect(reverse('clinic:receptionist'))

def receptionist_new_appointment(request, pesel):
    if not request.user.is_authenticated or \
        not Employee.objects.get(user = request.user).privilege == Employee.Position.RECEPTIONIST:
        return HttpResponseNotFound(not_found_html)    

    if request.method == 'POST':
        form = NewAppointmentForm(request.POST)
        if form.is_valid():

            time_choices = [(x,y) for (x,y) in Appointment.POSSIBLE_TIMES if x not in
                [z.time for z in Appointment.objects.filter(date=form.cleaned_data['date'])
                                                    .filter(doctor=form.cleaned_data['doctor'])]]

            if len(time_choices) == 0:
                return render(request, 'clinic/receptionist_new_appointment.html',
                    {'form':form, 'pesel':pesel, 'message': "This day is full."})

            formTime = NewAppointmentFormTime(time_choices,
                initial={'doctor': form.cleaned_data['doctor'],
                'treatment': form.cleaned_data['treatment'],
                'date': form.cleaned_data['date']})

            return render(request, 'clinic/receptionist_new_appointment_time.html',
                {'form':formTime, 'pesel':pesel})

    form = NewAppointmentForm()
    return render(request, 'clinic/receptionist_new_appointment.html', {'form':form, 'pesel':pesel})

def receptionist_new_appointment_time(request, pesel):
    if not request.user.is_authenticated or \
        not Employee.objects.get(user = request.user).privilege == Employee.Position.RECEPTIONIST:
        return HttpResponseNotFound(not_found_html)  

    if request.method == 'POST':
        form = NewAppointmentFormTime(Appointment.POSSIBLE_TIMES, request.POST)
        if form.is_valid():
            try:
                patient = Patient.objects.get(pesel = pesel)
                appointment = Appointment(patient = patient,
                    doctor = form.cleaned_data['doctor'],
                    date = form.cleaned_data['date'],
                    time = form.cleaned_data['time'],
                    treatment = form.cleaned_data['treatment'])

                appointment.save()
                return HttpResponseRedirect(reverse('clinic:patient', args=(pesel,)))

            except(Patient.DoesNotExist):
                return render(request, 'clinic/receptionist.html', {
                'form': form,
                'message': "We have no patient with a given PESEL"
            })

    return HttpResponseBadRequest(bed_request_html)

def receptionist_appointment_details(request, appointment_id):
    if not request.user.is_authenticated or \
        not Employee.objects.get(user = request.user).privilege == Employee.Position.RECEPTIONIST:
        return HttpResponseNotFound(not_found_html)  
    
    appointment = Appointment.objects.get(id = appointment_id)

    form = AppointmentReadOnlyForm(initial = {
        'doctor': appointment.doctor,
        'treatment': appointment.treatment,
        'date': appointment.date,
        'time': appointment.get_time_display(),
        'results': appointment.results
    })
    if len(appointment.results) == 0:
        form.mark_results_as_empty()
    return render(request, 'clinic/receptionist_appointment.html',
        {'form':form, 'pesel':appointment.patient.pesel,
        'appointment_id':appointment.id})

def receptionist_remove_appointment(request, appointment_id):
    if not request.user.is_authenticated or \
        not Employee.objects.get(user = request.user).privilege == Employee.Position.RECEPTIONIST:
        return HttpResponseNotFound(not_found_html)
        
    appointment = Appointment.objects.get(id = appointment_id)
    pesel = appointment.patient.pesel
    appointment.delete()
    return HttpResponseRedirect(reverse('clinic:patient', args=(pesel,)))


class ReceptionistView(generic.DetailView):
    model = Employee
    template_name = 'clinic/receptionist.html'