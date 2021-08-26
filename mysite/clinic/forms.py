import datetime
from django import forms
from .models import Employee, Treatment, Appointment

class LoginForm(forms.Form):
    login = forms.CharField(max_length = 100, widget=forms.TextInput(
        attrs={'class':'form-control', 'aria-describedby':'loginHelps'}))
    password = forms.CharField(max_length = 100, widget = forms.PasswordInput(
        attrs={'class':'form-control', 'aria-describedby':'wrongPasswords'}))


class NewEmployeeForm(forms.Form):
    login = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control', 'aria-describedby':'busyLogin'}
    ))
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    lastname = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    address = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    phone = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    salary = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class':'form-control'}
    ))
    password = forms.CharField(max_length=100, widget= forms.PasswordInput(
        attrs={'class':'form-control'}
    ))
    repeat_password = forms.CharField(max_length=100, widget = forms.PasswordInput(
        attrs={'class':'form-control', 'aria-describedby':'notTheSamePassword'}
    ))
    position = forms.ChoiceField(choices=Employee.Position.choices, widget = forms.Select(
        attrs={'class':'form-select'}
    ))

class EmployeeForm(NewEmployeeForm):
    login = forms.CharField(max_length=100, widget=forms.TextInput(
                attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    password = None
    repeat_password = None

class ChangePasswordForm(NewEmployeeForm):
    login = None
    name = None
    lastname = None
    address = None
    phone = None
    salary = None
    position = None
    
class EmployeeReadOnlyForm(forms.Form):        
    login = forms.CharField(max_length=100, widget=forms.TextInput(
                attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    name = forms.CharField(max_length=100, widget=forms.TextInput(
                attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    lastname = forms.CharField(max_length=100, widget=forms.TextInput(
                attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    address = forms.CharField(max_length=100, widget=forms.TextInput(
                attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    phone = forms.CharField(max_length=100, widget=forms.TextInput(
                attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    salary = forms.IntegerField(widget=forms.NumberInput(
                attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    position = forms.CharField(max_length=100, widget = forms.TextInput(
                attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))


class NewTreatmentForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control', 'aria-describedby':'busyName'}
    ))

    informations = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ), required=False)

    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class':'form-control'}
    ))

    refundable = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class':'form-check-input'}
    ), required=False)

class TreatmentForm(NewTreatmentForm):
    pass

class TreatmentReadOnlyForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))

    informations = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ), required=False)

    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))

    refundable = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext', 'disabled':'True'}
    ), required=False)    

class FindPatientForm(forms.Form):
    pesel = forms.CharField(max_length=11, min_length=11, widget=forms.TextInput(
        attrs={'class':'form-control', 'aria-describedby':'noPatient', 'placeholder':'PESEL'}
    ))

class NewPatientForm(forms.Form):
    pesel = forms.CharField(max_length = 11, min_length=11, widget=forms.TextInput(
        attrs={'class':'form-control', 'aria-describedby':'patientInDatabase'}
    ))
    name = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    lastname = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    address = forms.CharField(max_length = 100, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    phone_number = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

class PatientForm(forms.Form):
    pesel = forms.CharField(max_length = 11, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    name = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    lastname = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    address = forms.CharField(max_length = 100, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))
    phone_number = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'class':'form-control'}
    ))

class PatientReadOnlyForm(forms.Form):
    pesel = forms.CharField(max_length = 11, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    name = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    lastname = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    address = forms.CharField(max_length = 100, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    phone_number = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))

class DoctorModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '{} {}'.format(obj.name, obj.last_name)

class NewAppointmentForm(forms.Form):
    doctor = DoctorModelChoiceField(queryset=None, widget = forms.Select(
        attrs={'class':'form-select'}
    ))
    treatment = forms.ModelChoiceField(queryset=None, to_field_name='name', widget = forms.Select(
        attrs={'class':'form-select'}
    ))
    date = forms.DateField(widget = forms.DateInput(
        attrs={'class':'form-control', 'type': 'date', 'aria-describedby':'wrongDate'}
    ))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['treatment'].queryset = Treatment.objects.all()
        self.fields['doctor'].queryset = Employee.objects.all().filter(privilege = 'doctor')


class NewAppointmentFormTime(forms.Form):
    doctor = DoctorModelChoiceField(queryset=None, to_field_name='last_name', widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    treatment = forms.ModelChoiceField(queryset=None, to_field_name='name', widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    date = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    time = forms.ChoiceField(choices = Appointment.POSSIBLE_TIMES, widget = forms.Select(
            attrs={'class':'form-select'}
        ))

    def __init__(self, time_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['treatment'].queryset = Treatment.objects.all()
        self.fields['doctor'].queryset = Employee.objects.all()
        self.fields['time'].choices = time_choices


class AppointmentReadOnlyForm(forms.Form):
    doctor = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    treatment = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    date = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    time = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    results = forms.CharField(max_length = 64, widget=forms.Textarea(
        attrs={'readonly':'True', 'class':'form-control-plaintext', 'rows':'5'}
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def mark_results_as_empty(self):
        self.fields['results'].widget.attrs.update({'class':'form-control'})        

class AppointmentResultsForm(forms.Form):

    patient = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    treatment = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    date = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    time = forms.CharField(max_length = 64, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    informations = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'readonly':'True', 'class':'form-control-plaintext'}
    ))
    results = forms.CharField(max_length = 64, widget=forms.Textarea(
        attrs={'class':'form-control', 'rows':'5'}
    ))