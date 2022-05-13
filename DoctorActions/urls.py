from django.urls import path
from . import views



app_name = 'DoctorActions'

urlpatterns = [

    #DOCTOR~ACCEPT~RESERVATION~ENDPOINT------/action/dr/reservation/accept/
    #DOCTOR~REFUSE~RESERVATION~ENDPOINT------/action/dr/reservation/refuse/
    path('reservation/accept/', views.AcceptReservation, name="AcceptReservation"),
    path('reservation/refuse/', views.RefuseReservation, name="RefuseReservation"),

    #DOCTOR~CREATE~CLINIC~ENDPOINT----/action/dr/clinic/create/
    #DOCTOR~UPDATE~CLINIC~ENDPOINT----/action/dr/clinic/update/
    path('clinic/create/', views.CreateClinic, name="CreateClinic"),
    path('clinic/update/', views.UpdateClinic, name="UpdateClinic"),

    #DOCTOR~APPOINTMENTS~ENDPOINT-----/action/dr/appointments/
    path('appointments/', views.ViewAppointments, name="ViewAppointments"),

    #VIEW~PATIENT~PROFILE~ENDPOINT--/action/dr/patients/21
    path('patients/<int:id>/', views.ViewPatientProfile, name="ViewPatientProfile"), 
]