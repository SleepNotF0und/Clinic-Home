from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views



app_name = 'Users'

urlpatterns = [
    #SHOW~DOCTORS~BY~CATEGORY~ENDPOINT
    #SHOW~ALL~TOPICS~ENDPOINT
    #VIEW~TOPIC~ENDPOINT
    path('category/', views.DoctorsCategory, name="category"),
    path('topics/', views.AllTopics, name="topics"),
    path('topics/<int:id>', views.ViewTopic, name="topic"),


    #EMAIL~VALIDATION~ENDPOINT
    #MOBILE~VALIDATION~ENDPOINT
    #OPT~VALIDATION~ENDPOINT
    path('verify_email/', views.Verify_Email, name="VerifyEmail"),
    path('verify_mobile/', views.Verify_Mobile, name="VerifyOTP"),
    path('verify_OTP/', views.Verify_OTP, name="VerifyOTP"),


    #SIGN~UP~ENDPOINTS
    path('doctor/SignUp/', views.Create_Doctor, name="CreateDoctor"),
    path('patient/SignUp/', views.Create_Patient, name="CreatePatient"),


    #AUTH~TOKEN~BUILT-IN~ENDPOINT
    path('AuthToken/', obtain_auth_token), 


    #LOGIN~AUTH~TOKEN~ENDPOINT
    #FORGET~PASSWORD~ENDPOINT
    #RESET~PASSWORD~ENDPOINT
    #FACEBOOK~SOCIAL~LOGIN~ENDPOINT
    path('login/', views.Login, name="login"),
    path('login/ForgetPassword/', views.ForgetPassword, name="ForgetPassword"),
    path('login/ResetPassword/<int:id>', views.ResetPassword, name="PasswordReset"),
    path('login/FacebookAuth/', views.SocialLogin, name="FacebookLogin"),
]

