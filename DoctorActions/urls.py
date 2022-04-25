from django.urls import path
from . import views



app_name = 'DoctorActions'

urlpatterns = [

    #DOCTOR~ACCEPT~RESERVATION~ENDPOINT------/action/dr/reservation/accept/
    #DOCTOR~REFUSE~RESERVATION~ENDPOINT------/action/dr/reservation/refuse/
    path('reservation/accept/', views.AcceptReservation, name="AcceptReservation"),
    path('reservation/refuse/', views.RefuseReservation, name="RefuseReservation"),

    #DOCTOR~APPOINTMENTS~ENDPOINT-----/action/dr/appointments/
    path('appointments/', views.ViewAppointments, name="ViewAppointments"),
]