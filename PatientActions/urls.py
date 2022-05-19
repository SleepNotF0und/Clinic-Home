from django.urls import path
from . import views



app_name = 'PatientActions'

urlpatterns = [

    #SEARCH~ANY~USER~BY~NAME~ENDPOINT------/action/pt/search/name/?search=admin
    #SEARCH~DOCTOR~ONLY~BY~CITY~ENDPOINT------/action/pt/search/city/?search=r
    #SEARCH~CLINIC~BY~CITY~ENDPOINT------/action/pt/search/clinic/city/?search=tes
    path('search/name/', views.SearchByName.as_view()),
    path('search/clinic/city/', views.SearchClinicByCity.as_view()),

    
    #VIEW~DOCTOR~PROFILE~ENDPOINT--/action/pt/drs/21/
    #VIEW~DOCTOR~CLINICS~ENDPOINT--/action/pt/drs/21/clinics/
    #VIEW~CLINIC~PAGE~ENDPOINT--/action/pt/clinics/3/
    #VIEW~TOP~RATED~ENDPOINT---/action/pt/drs/topRated/
    path('drs/<int:id>/', views.ViewDoctorProfile, name="ViewDoctorProfile"),
    path('drs/<int:id>/clinics/', views.ViewDoctorClinics, name="ViewDoctorClinics"),
    path('clinics/<int:id>/', views.ViewClinic, name="ViewClinic"),
    path('drs/TopRated/', views.TopRated, name="TopRated"),

    
    #RESERVE~ENDPOINT----/action/pt/reserve/create/
    #DELETE~RESERVE~ENDPOINT---/action/pt/reserve/delete/
    #VIEW~PATIENT~RESERVATIONS-----/action/pt/reservations/
    path('reservation/create/', views.Reserve, name="CreateReservation"),
    path('reservation/delete/', views.DeleteReserve, name="DeleteReservation"),
    path('reservations/', views.ViewReservations, name="ViewReservations"),


    #COMMENT~ENDPOINT---/action/pt/comment/create/
    #DELETE~COMMENT~ENDPOINT---/action/pt/comment/delete/
    path('comment/create/', views.Comment, name="CreateComment"),
    path('comment/delete/', views.DeleteComment, name="DeleteComment"),


    #THANKS~ENDPOINT----/action/pt/add/thanks/
    #PREVIEW~ENDPOINT---/action/pt/add/preview/
    path('add/thanks/', views.MakeThanks, name="MakeThanks"),
    path('add/preview/', views.MakePreview, name="MakePreview"),
    path('undo/thanks/', views.UndoThanks, name="UndoThanks"),
    path('undo/preview/', views.UndoPreview, name="UndoPreview"),

]
