from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views



app_name = 'Users'

urlpatterns = [
    #SHOW~DOCTORS~SPEC~INFO~ENDPOINT
    path('doctors/dentist/', views.GET_DentistInfo, name="GET_DentistInfo"),
    path('doctors/internalMedicine/', views.GET_InternalInfo, name="GET_InternalInfo"),
    path('doctors/ophthalmologists/', views.GET_OphthalmologistsInfo, name="GET_OphthalmologistsInfo"),
    path('doctors/pediatricians/', views.GET_PediatriciansInfo, name="GET_PediatriciansInfo"),
    path('doctors/otolaryngologists/', views.GET_OtolaryngologistsInfo, name="GET_OtolaryngologistsInfo"),
    path('doctors/dermatologists/', views.GET_DermatologistsInfo, name="GET_DermatologistsInfo"),
    path('doctors/neurologists/', views.GET_NeurologistsInfo, name="GET_NeurologistsInfo"),
    path('doctors/gynecologists/', views.GET_GynecologistsInfo, name="GET_GynecologistsInfo"),



    #EMAIL~VALIDATION~ENDPOINT
    path('doctor/verify_email/', views.Verify_Email, name="VerifyEmail"),
    path('patient/verify_email/', views.Verify_Email, name="VerifyEmail"),

    #EMAIL~OTP~VALIDATION~ENDPOINT
    path('doctor/verify_email/verify_OTP/', views.Verify_OTP, name="VerifyOTP"),
    path('patient/verify_email/verify_OTP/', views.Verify_OTP, name="VerifyOTP"),


    #MOBILE~VALIDATION~ENDPOINT
    path('doctor/verify_mobile/', views.Verify_Mobile, name="VerifyOTP"),
    path('patient/verify_mobile/', views.Verify_Mobile, name="VerifyOTP"),

    #MOBILE~OTP~VALIDATION~ENDPOINT
    path('doctor/verify_mobile/verify_OTP/', views.Verify_OTP, name="VerifyOTP"),
    path('patient/verify_mobile/verify_OTP/', views.Verify_OTP, name="VerifyOTP"),


    #SIGN~UP~ENDPOINTS
    path('doctor/SignUp/', views.Create_Doctor, name="CreateDoctor"),
    path('patient/SignUp/', views.Create_Patient, name="CreatePatient"),


    #AUTH~TOKEN~BUILT-IN~ENDPOINT
    path('AuthToken/', obtain_auth_token), 

    #LOGIN~AUTH~TOKEN~ENDPOINT
    path('Login/', views.Login, name="Login"),

    #FORGET~PASSWORD~ENDPOINT
    path('Login/ForgetPassword/', views.ForgetPassword, name="ForgetPassword"),

    #RESET~PASSWORD~ENDPOINT
    path('Login/ResetPassword/<int:id>', views.ResetPassword, name="PasswordReset"),

    #FACEBOOK~SOCIAL~LOGIN~ENDPOINT
    path('Login/FacebookAuth/', views.SocialLogin, name="FacebookLogin"),
]

