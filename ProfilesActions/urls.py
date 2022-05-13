from django.urls import path
from . import views



app_name = 'ProfilesActions'

urlpatterns = [

    #PROFILES~ENDPOINT
    path('patient/', views.PtUserProfile, name="PtUserProfile"),
    path('doctor/', views.DrUserProfile, name="DrUserProfile"),

    
    #NOTIFICATIONS~ENDPOINTS
    path('Pt/notifications/', views.PtUserNotifications, name="PtUserNotifications"), 
    path('Dr/notifications/', views.DrUserNotifications, name="DrUserNotifications"),
    
    
    #PROFILE~SETTINGS~ENDPOINTS
    path('ImageUpdate/', views.ImageUpdate, name="ImageUpdate"),
    path('InfoUpdate/', views.InfoUpdate, name="InfoUpdate"),
    path('PasswordUpdate/', views.PasswordUpdate, name="PasswordUpdate"),

    path('patient/AddressUpdate/', views.PtAddressUpdate, name="PtAddressUpdate"),

    path('patient/SpecialInfoUpdate/', views.PtSpecialInfoUpdate, name="PtSpecialInfoUpdate"),
    path('doctor/SpecialInfoUpdate/', views.DrSpecialInfoUpdate, name="DrSpecialInfoUpdate"),
]

