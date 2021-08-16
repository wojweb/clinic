from django.urls import path
from . import views

app_name = 'clinic'

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
    path('admin/', views.AdminListView.as_view(), name='admin'),
    path('new_employee/', views.admin_new_employee, name='new_employee'),
    path('employee_details/<login>', views.admin_employee_details, name='employee_details'),
    path('employee_remove/<login>', views.admin_employee_remove, name='employee_remove'),
    path('employee_update/<login>', views.admin_employee_update, name='employee_update'),
    path('employee_change_password/<login>', views.admin_change_password, name='change_password'),
    path('admin_treatments/', views.TreatmentsListView.as_view(), name='treatments'),
    path('treatment_details/<name>', views.admin_treatment_details, name='treatment_details'),
    path('treatment_update/<name>', views.admin_treatment_update, name='treatment_update'),
    path('treatment_remove/<name>', views.admin_treatment_remove, name='treatment_remove'),
    path('new_treatment/', views.admin_new_treatment, name='new_treatment'),
    path('<pk>/doctor/', views.DoctorView.as_view(), name='doctor'),
    path('receptionist/', views.receptionist, name='receptionist'),
    path('new_patient/', views.receptionist_new_patient, name='new_patient'),
    path('patient/<pesel>', views.receptionist_patient, name='patient'),
    path('patient_update/<pesel>', views.receptionist_patient_update, name='patient_update'),
    path('patient_remove/<pesel>', views.receptionist_patient_remove, name='patient_remove'),
    path('new_appointment/<pesel>', views.receptionist_new_appointment, name='new_appointment'),
    path('receptionist_appointment_details', views.temp, name='receptionist_appointment_details'),
    path('test/', views.test, name='test'),
    path('temp/', views.temp, name='temp'),
    path('employees/', views.AdminListView.as_view(), name='employees'),
    # path('treatments/', views.temp, name='treatments'),
    # path('<pk>/details/', views.employee_details, name='employee_details'),
    path('<pk>/change_password', views.temp, name='employee_change_password')
]

