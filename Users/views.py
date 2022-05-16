from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext as _

from django.contrib.auth import authenticate, get_user_model

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from twilio.rest import Client

from .models import *
from .serializers import *

import random, os








@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def DoctorsCategory(request):
    if request.method == 'GET':
        Param = request.GET.get('spec', '')
        data = { 'Doctors': [] }
        doctors_db = Doctors.objects.all()
        DoctorsCategory_srz = DoctorsCategorySerializer(doctors_db, many=True)

        for ele in DoctorsCategory_srz.data:
            GetUser = CustomUser.objects.get(pk=ele['user'])          
            GetImage = GetUser.profile_pic

            if GetImage and hasattr(GetImage, 'url'):
                CurrentImage = GetImage.url
            else:
                CurrentImage = "User has No Profile Pic"
            
            if GetUser:
                ele['username'] = GetUser.username
                ele['image'] = CurrentImage
                if ele['specialize'] == Param:
                    data['Doctors'].append(ele)
        
        content = {"status":True, "details":"success", "data":data}
        return Response(content, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def AllTopics(request):
    if request.method == 'GET':
        topics_db = Topics.objects.all()
        topics_srz = AllTopicsSerializer(topics_db, many=True)

        content = {"status":True, "Topics":topics_srz.data}     
        return Response(content, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def ViewTopic(request, id):
    if request.method == 'GET':

        try:
            get_topic = Topics.objects.get(id=id)
        
            content = {
                "status":True,
                "title":get_topic.title, 
                "image_url":get_topic.topic_image.url, 
                "body":get_topic.body
                }     
            return Response(content, status=status.HTTP_200_OK)

        except Topics.DoesNotExist:
            content = {"status":False, "detials":"Topic not found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@authentication_classes(())
#========================
def Verify_Email(request):
    if request.method == 'POST':

        VerifyEmail_srz = VerifyEmailSerializer(data=request.data) 
        if VerifyEmail_srz.is_valid(raise_exception=True):

            email = VerifyEmail_srz.data['email']
            
            try:
                UserEmail = get_user_model().objects.get(email=email)

                if UserEmail.is_verified:
                    content = {"status":False, "details":"Email address already taken."}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                else:
                    #SEND~OTP~CODE~VIA~EMAIL
                    subject = UserEmail
                    OTP = random.randint(1000, 9999)
                    message = "Hello From Health+, Your OTP Code " + str(OTP)
                    email_form = settings.EMAIL_HOST
                    send_mail(subject, message, email_form, [email])

                    #SAVE~OTP~INTO~THE~USER~TABLE
                    UserEmail.otp = OTP
                    UserEmail.save()

                    content = {"status":True, "details":"Email address already taken But Not Verfied, OTP Code Sent to your Email."}
                    return Response(content, status=status.HTTP_201_CREATED)
            
            except get_user_model().DoesNotExist:
                OTP = str(random.randint(1000, 9999))
                UserEmail = get_user_model().objects.create(email=email, otp=OTP)
                UserEmail.save()

                #SEND~OTP~CODE~VIA~EMAIL
                subject = "clinic home"
                message = "Hello From Health+, Your OTP Code " + OTP
                email_form = settings.EMAIL_HOST
                send_mail(subject, message, email_form, [email])

                content = {"status":True, "details":"OTP Code Send to your Email."}
                return Response(content, status=status.HTTP_201_CREATED)

        else:
            content = {"status":False, "details":"serializer Error."}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authentication_classes(())
#========================
def Verify_Mobile(request):
    if request.method == 'POST':

        VerifyMobile_srz = VerifyMobileSerializer(data=request.data)
        if VerifyMobile_srz.is_valid(raise_exception=True):

            mobile = VerifyMobile_srz.data['mobile']
            
            try:
                UserMobile = get_user_model().objects.get(mobile=mobile)

                if UserMobile.is_verified:
                    content = {"status":False, "details":"Mobile number already taken."}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

                else:
                    OTP = str(random.randint(1000, 9999))

                    account_sid = 'ACed031bba4f307f38d7bc646440dda43b'
                    auth_token = '332363210ae724feb2fc08b400d65deb'

                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                                body='Hello From Health+, Your OTP is '+OTP,
                                from_='+17622310919',
                                to=UserMobile.mobile
                            )

                    UserMobile.otp = OTP
                    UserMobile.save()

                    content = {"status":True, "details":"Mobile already taken But Not Verfied, OTP Code Sent to your Mobile."}
                    return Response(content, status=status.HTTP_201_CREATED)
            
            except get_user_model().DoesNotExist:
                OTP = str(random.randint(1000, 9999))
                UserMobile = get_user_model().objects.create(mobile=mobile, email="WaitOTPmobile@test.com"+OTP, otp=OTP)
                UserMobile.save()

                account_sid = 'ACed031bba4f307f38d7bc646440dda43b'
                auth_token = '332363210ae724feb2fc08b400d65deb'

                client = Client(account_sid, auth_token)

                message = client.messages.create(
                            body='Hello From Health+, Your OTP is '+ OTP,
                            from_='+17622310919',
                            to=UserMobile.mobile
                        )

                content = {"status":True, "details":"OTP Code Send to your Mobile."}
                return Response(content, status=status.HTTP_201_CREATED)

        else:
            content = {"status":False, "details":"serializer Error"}        
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authentication_classes(())
#========================
def Verify_OTP(request):
    if request.method == 'POST':
        VerifyOTP_srz = VerifyOTPSerializer(data=request.data)

        if VerifyOTP_srz.is_valid(raise_exception=True):
            OTP = VerifyOTP_srz.data['otp']

            try:
                CurrentUser = CustomUser.objects.get(otp=OTP)

                if CurrentUser.otp == OTP:
                    CurrentUser.is_verified = True
                    CurrentUser.username = "OTP-Verified" 
                    CurrentUser.save()

                    #GET~USER~TOKEN~&~RETURN~IN~RESPONSE
                    Get_UserToken = Token.objects.get(user=CurrentUser.id)
                    Key = Get_UserToken.key

                    content = {"status":True, "details":"Valid OTP Code, Email Varified.", "token": Key.encode('utf-8')}
                    return Response(content, status=status.HTTP_201_CREATED)

                else:
                    content = {"status":False, "details":"Unvalid OTP Code."}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

            except get_user_model().DoesNotExist:
                content = {"status":False, "details":"Unvalid OTP Code."}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            content = {"status":False, "details":"serializer Error"}        
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authentication_classes(())
#========================
def Create_Doctor(request):
    if request.method == 'POST':
        DoctorCreate_srz = DoctorCreateSerializer(data=request.data) 

        if DoctorCreate_srz.is_valid(raise_exception=True):
            try:
                DoctorCreate_srz.save()

                content = {"status":True, "is_doctor":True, "details":"Account Created"}     
                return Response(content, status=status.HTTP_201_CREATED)

            except get_user_model().DoesNotExist:
                content = {"status":False, "details":"You Should First Pass Email Or Mobile Validation Endpoint !!"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            content = {"status":False, "details":"serializer Error"}     
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authentication_classes(())
#========================
def Create_Patient(request):
    if request.method == 'POST':
        PatientsCreate_srz = PatientCreateSerializer(data=request.data) 

        if PatientsCreate_srz.is_valid(raise_exception=True):
            try:
                PatientsCreate_srz.save()

                content = {"status":True, "is_patient":True, "details":"Account Created"}     
                return Response(content, status=status.HTTP_201_CREATED)
            
            except get_user_model().DoesNotExist:
                content = {"status":False, "details":"You Should First Pass Email Or Mobile Validation Endpoint !!"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            content = {"status":False, "details":"serializer Error"}     
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@authentication_classes(())
#========================
#LOGIN~VIEW~DOEN'T~HAVE~SERIALIZER
def Login(request):
    if request.method == 'POST':         
        
        Email = request.data['email']
        Password = request.data['password']

        try:
            GetUser = get_user_model().objects.get(email=Email)
            if Password == GetUser.password:

                Get_UserToken = Token.objects.get(user=GetUser.id)
                Key = Get_UserToken.key
                
                if GetUser.is_doctor == True:
                    UserAcc = 'Doctor'
                elif GetUser.is_patient == True:
                    UserAcc = 'Patient'

                content = {'status':True, 'token': Key.encode('utf-8'), 'username':GetUser.username, 'role':UserAcc}    
                return Response(content, status=status.HTTP_201_CREATED)

            else:
                content = {"status":False, "details":"Wrong Password"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User Not Found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@authentication_classes(())
#========================
def ForgetPassword(request):
    if request.method == 'POST':
        Email = request.data['email']
        
        try:
            CurrentUser = get_user_model().objects.get(email=Email)

            #SEND~OTP~CODE~VIA~EMAIL
            subject = Email
            message = "Hello From Health+, Here is your OTP "+str(CurrentUser.otp)+" to Reset Your Password"
            email_form = settings.EMAIL_HOST
            send_mail(subject, message, email_form, [Email])

            content = {"status":True, "details":"Reset Password Email Sent to Your Email"}
            return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:               
            content = {"status":False, "details":"No User Found With the Provided Email."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes(())
#========================
#ResetPassword()~VIEW~DOESN'T~HAVE~A~SERIALIZER
def ResetPassword(request, id):  
    if request.method == 'POST':

        try:
            CurrentUser = get_user_model().objects.get(id=id)
            UserOTP = CurrentUser.otp
            
            OTP = request.data['otp']
            NewPassword = request.data['password']
            ReNewPassword = request.data['re-password']

            if OTP != UserOTP:
                content = {"status":False, "details":"OTP Not valid"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            elif NewPassword != ReNewPassword:
                content = {"status":False, "details":"Passwords didn't Match"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            else:
                CurrentUser.password = NewPassword
                CurrentUser.save()

                content = {"status":True, "details":"Password Reseted"}     
                return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User ID Not Found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)

 

@api_view(['POST'])
@authentication_classes(())
#========================
def SocialLogin(request): 
    if request.method == 'POST':
        FacebookSocialAuth_srz = FacebookSocialAuthSerializer(data=request.data)
        FacebookSocialAuth_srz.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


