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

from .models import Doctors, Patients
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
    


# @api_view(['GET'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# #========================
# def GET_InternalInfo(request):
#     if request.method == 'GET':

#         data = { 'Doctors': [] }
#         doctors_db = Doctors.objects.all()
#         InternalInfo_srz = InternalInfoSerializer(doctors_db, many=True)
        
#         for ele in InternalInfo_srz.data:     
#             GetUser = CustomUser.objects.get(pk=ele['user'])
#             GetImage = GetUser.profile_pic

#             if GetImage and hasattr(GetImage, 'url'):
#                 CurrentImage = GetImage.url
#             else:
#                 CurrentImage = "User has No Profile Pic"

#             if GetUser:
#                 ele['username'] = GetUser.username
#                 ele['image'] = CurrentImage
#                 if ele['specialize'] == 'internal medicine':
#                     data['Doctors'].append(ele)
                
#         content = {"status":True, "details":"success", "data":data}
#         return Response(content, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# #========================
# def GET_OphthalmologistsInfo(request):
#     if request.method == 'GET':

#         data = { 'Doctors': [] }
#         doctors_db = Doctors.objects.all()
#         OphthalmologistsInfo_srz = OphthalmologistsInfoSerializer(doctors_db, many=True)
        
#         for ele in OphthalmologistsInfo_srz.data:     
#             GetUser = CustomUser.objects.get(pk=ele['user'])
#             GetImage = GetUser.profile_pic

#             if GetImage and hasattr(GetImage, 'url'):
#                 CurrentImage = GetImage.url
#             else:
#                 CurrentImage = "User has No Profile Pic"

#             if GetUser:
#                 ele['username'] = GetUser.username
#                 ele['image'] = CurrentImage
#                 if ele['specialize'] == 'ophthalmologists':
#                     data['Doctors'].append(ele)
                
#         content = {"status":True, "details":"success", "data":data}
#         return Response(content, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# #========================
# def GET_PediatriciansInfo(request):
#     if request.method == 'GET':

#         data = { 'Doctors': [] }
#         doctors_db = Doctors.objects.all()
#         PediatriciansInfo_srz = PediatriciansInfoSerializer(doctors_db, many=True)
        
#         for ele in PediatriciansInfo_srz.data:     
#             GetUser = CustomUser.objects.get(pk=ele['user'])
#             GetImage = GetUser.profile_pic

#             if GetImage and hasattr(GetImage, 'url'):
#                 CurrentImage = GetImage.url
#             else:
#                 CurrentImage = "User has No Profile Pic"

#             if GetUser:
#                 ele['username'] = GetUser.username
#                 ele['image'] = CurrentImage
#                 if ele['specialize'] == 'pediatricians':
#                     data['Doctors'].append(ele)
                
#         content = {"status":True, "details":"success", "data":data}
#         return Response(content, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# #========================
# def GET_OtolaryngologistsInfo(request):
#     if request.method == 'GET':

#         data = { 'Doctors': [] }
#         doctors_db = Doctors.objects.all()
#         OtolaryngologistsInfo_srz = OtolaryngologistsInfoSerializer(doctors_db, many=True)
        
#         for ele in OtolaryngologistsInfo_srz.data:     
#             GetUser = CustomUser.objects.get(pk=ele['user'])
#             GetImage = GetUser.profile_pic

#             if GetImage and hasattr(GetImage, 'url'):
#                 CurrentImage = GetImage.url
#             else:
#                 CurrentImage = "User has No Profile Pic"

#             if GetUser:
#                 ele['username'] = GetUser.username
#                 ele['image'] = CurrentImage
#                 if ele['specialize'] == 'otolaryngologists':
#                     data['Doctors'].append(ele)
                
#         content = {"status":True, "details":"success", "data":data}
#         return Response(content, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# #========================
# def GET_DermatologistsInfo(request):
#     if request.method == 'GET':

#         data = { 'Doctors': [] }
#         doctors_db = Doctors.objects.all()
#         DermatologistsInfo_srz = DermatologistsInfoSerializer(doctors_db, many=True)
        
#         for ele in DermatologistsInfo_srz.data:     
#             GetUser = CustomUser.objects.get(pk=ele['user'])
#             GetImage = GetUser.profile_pic

#             if GetImage and hasattr(GetImage, 'url'):
#                 CurrentImage = GetImage.url
#             else:
#                 CurrentImage = "User has No Profile Pic"

#             if GetUser:
#                 ele['username'] = GetUser.username
#                 ele['image'] = CurrentImage
#                 if ele['specialize'] == 'dermatologists':
#                     data['Doctors'].append(ele)
                
#         content = {"status":True, "details":"success", "data":data}
#         return Response(content, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# #========================
# def GET_NeurologistsInfo(request):
#     if request.method == 'GET':

#         data = { 'Doctors': [] }
#         doctors_db = Doctors.objects.all()
#         NeurologistsInfo_srz = NeurologistsInfoSerializer(doctors_db, many=True)
        
#         for ele in NeurologistsInfo_srz.data:     
#             GetUser = CustomUser.objects.get(pk=ele['user'])
#             GetImage = GetUser.profile_pic

#             if GetImage and hasattr(GetImage, 'url'):
#                 CurrentImage = GetImage.url
#             else:
#                 CurrentImage = "User has No Profile Pic"

#             if GetUser:
#                 ele['username'] = GetUser.username
#                 ele['image'] = CurrentImage
#                 if ele['specialize'] == 'neurologists':
#                     data['Doctors'].append(ele)
                
#         content = {"status":True, "details":"success", "data":data}
#         return Response(content, status=status.HTTP_200_OK)



# @api_view(['GET'])
# @authentication_classes((TokenAuthentication,))
# @permission_classes((IsAuthenticated,))
# #========================
# def GET_GynecologistsInfo(request):
#     if request.method == 'GET':

#         data = { 'Doctors': [] }
#         doctors_db = Doctors.objects.all()
#         GynecologistsInfo_srz = GynecologistsInfoSerializer(doctors_db, many=True)
        
#         for ele in GynecologistsInfo_srz.data:     
#             GetUser = CustomUser.objects.get(pk=ele['user'])
#             GetImage = GetUser.profile_pic

#             if GetImage and hasattr(GetImage, 'url'):
#                 CurrentImage = GetImage.url
#             else:
#                 CurrentImage = "User has No Profile Pic"

#             if GetUser:
#                 ele['username'] = GetUser.username
#                 ele['image'] = CurrentImage
#                 if ele['specialize'] == 'gynecologists':
#                     data['Doctors'].append(ele)
                
#         content = {"status":True, "details":"success", "data":data}
#         return Response(content, status=status.HTTP_200_OK)





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
                UserEmail = get_user_model().objects.create_user(email=email, username="WaitOtpEmail")
                
                #SEND~OTP~CODE~VIA~EMAIL
                subject = UserEmail
                OTP = str(random.randint(1000, 9999))
                message = "Hello From Health+, Your OTP Code " + OTP
                email_form = settings.EMAIL_HOST
                send_mail(subject, message, email_form, [email])

                #SAVE~OTP~INTO~THE~USER~TABLE
                UserEmail.otp = OTP
                UserEmail.save()

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
                UserMobile = get_user_model().objects.create_user(mobile=mobile, username="WaitOtpMobile")

                OTP = str(random.randint(1000, 9999))

                account_sid = 'ACed031bba4f307f38d7bc646440dda43b'
                auth_token = '332363210ae724feb2fc08b400d65deb'

                client = Client(account_sid, auth_token)

                message = client.messages.create(
                            body='Hello From Health+, Your OTP is '+ OTP,
                            from_='+17622310919',
                            to=UserMobile.mobile
                        )
                
                UserMobile.otp = OTP
                UserMobile.save()

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
                CurrentUser = get_user_model().objects.get(username="WaitOtpEmail")
                
                if CurrentUser.otp == OTP:
                    CurrentUser.is_verified = True
                    CurrentUser.save()

                    content = {"status":True, "details":"Valid OTP Code, Email Varified."}
                    return Response(content, status=status.HTTP_201_CREATED)

                else:
                    content = {"status":False, "details":"Unvalid OTP Code."}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

            except get_user_model().DoesNotExist:
                CurrentUser = get_user_model().objects.get(username="WaitOtpMobile")
                
                if CurrentUser.otp == OTP:
                    CurrentUser.is_verified = True
                    CurrentUser.save()

                    content = {"status":True, "details":"Valid OTP Code, Mobile Varified."}
                    return Response(content, status=status.HTTP_201_CREATED)

                else:
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
            DoctorCreate_srz.save()

            content = {"status":True, "is_doctor":True, "details":"Account Created"}     
            return Response(content, status=status.HTTP_201_CREATED)

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
            PatientsCreate_srz.save()

            content = {"status":True, "is_patient":True, "details":"Account Created"}     
            return Response(content, status=status.HTTP_201_CREATED)

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

                content = {'status':True, 'token': Key.encode('utf-8'), 'Username':GetUser.username, 'Account Type':UserAcc}    
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
            message = "Hello From Health+, Visit this Link to Reset Your Password http://127.0.0.1:8000/api/login/ResetPassword/"+str(CurrentUser.id)
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

            NewPassword = request.data['password']
            ReNewPassword = request.data['re-password']

            if NewPassword == ReNewPassword:
                CurrentUser.password = NewPassword
                CurrentUser.save()

                content = {"status":True, "details":"Password Reseted"}     
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                content = {"status":False, "details":"Passwords didn't Match"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
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



'''
@api_view(['GET','PUT','DELETE'])
def PUT_DEL_Doctors(request, id):
    try:
        doctors_db = Doctors.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        doctors_srz = DoctorSerializer(doctors_db, many=False)
        return Response(doctors_srz.data)

    elif request.method == 'PUT':
        doctors_srz = DoctorSerializer(doctors_db, data=request.data) 
        return Response(doctors_srz.data)

    if request.method == 'DELETE':
        doctors_db.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
'''


















