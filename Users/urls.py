from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views



app_name = 'Users'

urlpatterns = [
    #SHOW~DOCTORS~BY~CATEGORY~ENDPOINT-------/api/category/?spec=neurologists
    #SHOW~ALL~TOPICS~ENDPOINT
    #VIEW~TOPIC~ENDPOINT
    path('category/', views.DoctorsCategory, name="category"),
    path('topics/', views.AllTopics, name="topics"),
    path('topics/<int:id>/', views.ViewTopic, name="topic"),


    #EMAIL~VALIDATION~ENDPOINT
    #EMAIL~OTP~VALIDATION~ENDPOINT
    #MOBILE~OTP~VALIDATION~ENDPOINT
    path('verify/email/', views.Verify_Email, name="VerifyEmail"),
    path('verify/otp/email/', views.Email_OTP_Verify, name="Email_OTP_Verify"),
    path('verify/otp/mobile/', views.Mobile_OTP_Verify, name="Mobile_OTP_Verify"),


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
    path('login/ResetPassword/', views.ResetPassword, name="PasswordReset")
]

