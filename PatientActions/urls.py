from django.urls import path
from . import views



app_name = 'PatientActions'

urlpatterns = [

    #SEARCH~BY~NAME~ENDPOINT------/action/pt/search/name/?search=admin
    #SEARCH~BY~CITY~ENDPOINT------/action/pt/search/city/?search=r
    path('search/name/', views.SearchByName.as_view()),
    path('search/city/', views.SearchByCity.as_view()),

    
    #VIEW~DOCTOR~PROFILE~ENDPOINT--/action/pt/dr/21
    path('drs/<int:id>/', views.ViewDoctorProfile, name="ViewDoctorProfile"),    

    
    #RESERVE~ENDPOINT----/action/pt/reserve/create/
    #DELETE~RESERVE~ENDPOINT---/action/pt/reserve/delete/
    path('reserve/create/', views.Reserve, name="CreateReservation"),
    path('reserve/delete/', views.DeleteReserve, name="DeleteReservation"),


    #COMMENT~ENDPOINT---/action/pt/comment/create/
    #DELETE~COMMENT~ENDPOINT---/action/pt/comment/delete/
    path('comment/create/', views.Comment, name="CreateComment"),
    path('comment/delete/', views.DeleteComment, name="DeleteComment"),


    #VIEW~PATIENT~RESERVATIONS-----/action/pt/reservations/
    path('reservations/', views.ViewReservations, name="ViewReservations"),





    #DEBUG~ALL~RESERVATIONS~ENDPOINT
    path('Reservations/', views.GET_Reservations, ),
]
