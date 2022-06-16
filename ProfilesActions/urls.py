from django.urls import path
from django.urls.conf import re_path

from . import views
from .views import ProfileImageUpload



app_name = 'ProfilesActions'

urlpatterns = [

    #PROFILES~ENDPOINT
    path('patient/', views.PtUserProfile, name="PtUserProfile"),
    path('doctor/', views.DrUserProfile, name="DrUserProfile"),

    
    #NOTIFICATIONS~ENDPOINTS
    path('Pt/notifications/', views.PtUserNotifications, name="PtUserNotifications"), 
    path('Dr/notifications/', views.DrUserNotifications, name="DrUserNotifications"),
    
    
    #PROFILE~SETTINGS~ENDPOINTS
    path('ImageUpdate/', ProfileImageUpload.as_view(), name="ProfileImageUpload"),
    path('InfoUpdate/', views.InfoUpdate, name="InfoUpdate"),
    path('PasswordUpdate/', views.PasswordUpdate, name="PasswordUpdate"),

    path('patient/AddressUpdate/', views.PtAddressUpdate, name="PtAddressUpdate"),

    path('patient/SpecialInfoUpdate/', views.PtSpecialInfoUpdate, name="PtSpecialInfoUpdate"),
    path('doctor/SpecialInfoUpdate/', views.DrSpecialInfoUpdate, name="DrSpecialInfoUpdate"),


    #CHATS~ENDPOINTS 
    path('pt/message/send/', views.PtSendMessage, name="PtSendMessage"),
    path('dr/message/send/', views.DrSendMessage, name="DrSendMessage"),

    path('pt/mychat/', views.PtChatList, name="PtChatList"),
    path('dr/mychat/', views.DrChatList, name="DrChatList"),

    path('pt/chat/', views.PtChatWith, name='PtChatWith'),
    path('dr/chat/', views.DrChatWith, name='DrChatWith'),
]

