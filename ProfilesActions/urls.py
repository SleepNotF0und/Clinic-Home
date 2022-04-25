from django.urls import path
from . import views



app_name = 'ProfilesActions'

urlpatterns = [

    #PATIENT~PROFILE
    path('Pt/', views.PtUserProfile, name="PtUserProfile"),

    #DOCTOR~PROFILE
    path('Dr/', views.DrUserProfile, name="DrUserProfile"), 
    
    #PROFILE~SETTINGS
    path('ImageUpdate/', views.ImageUpdate, name="ImageUpdate"),
    path('InfoUpdate/', views.InfoUpdate, name="InfoUpdate"),
    path('PasswordUpdate/', views.PasswordUpdate, name="PasswordUpdate"),

    path('patient/AddressUpdate/', views.PtAddressUpdate, name="PtAddressUpdate"),
    path('doctor/AddressUpdate/', views.DrAddressUpdate, name="DrAddressUpdate"),

    path('patient/SpecialInfoUpdate/', views.PtSpecialInfoUpdate, name="PtSpecialInfoUpdate"),
    path('doctor/SpecialInfoUpdate/', views.DrSpecialInfoUpdate, name="DrSpecialInfoUpdate"),
]

