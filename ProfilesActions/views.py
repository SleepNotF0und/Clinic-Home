from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

import cloudinary.uploader

from Users.models import Doctors, Patients
from PatientActions.models import Reservations
from .models import Notifications

from .serializers import *









@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def PtUserProfile(request):
    if request.method == 'GET':
        CurrentUser = request.user
        GetImage = CurrentUser.profile_pic

        #CHECK~IF~USER~HAVE~PROFILE~PIC
        if GetImage and hasattr(GetImage, 'url'):
            CurrentImage = GetImage.url
        else:
            CurrentImage = "User has No Profile Pic"

        GetPatient = Patients.objects.filter(user=CurrentUser)
        PtProfile_srz = PtProfileSerializer(GetPatient, many=True)

    content = {
        "status":True, 
        "username":CurrentUser.username, 
        "ImageURL":CurrentImage,
        "info":PtProfile_srz.data
        }
    return Response(content, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def DrUserProfile(request):
    if request.method == 'GET':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            GetImage = CurrentUser.profile_pic

            GetDoctor = Doctors.objects.get(user=GetUser.id)

            #CHECK~IF~DOCTOR~HAVE~PROFILE~PIC
            if GetImage and hasattr(GetImage, 'url'):
                CurrentImage = GetImage.url
            else:
                CurrentImage = "User has No Profile Pic"

            content = {
                "status":True, 
                "username":CurrentUser.username, 
                "imageURL":CurrentImage, 
                "info":GetDoctor.info,
                "gender":GetDoctor.gender,
                "date of birth":GetDoctor.dateofbirth,
                "specialize":GetDoctor.specialize, 
                "price":GetDoctor.price
                }
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def DrUserNotifications(request):
    if request.method == 'GET':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            GetDoctor = Doctors.objects.get(user=GetUser.id)

            GetDrNotifications = Notifications.objects.filter(doctor=GetDoctor)
            GetDrNotifications_srz = GetDrNotificationsSerializer(GetDrNotifications, many=True)

            content = {
                "status":True, 
                "username":CurrentUser.username, 
                "notifications":GetDrNotifications_srz.data
                }
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def PtUserNotifications(request):
    if request.method == 'GET':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            GetPatient = Patients.objects.get(user=GetUser.id)

            GetPtNotifications = Notifications.objects.filter(patient=GetPatient)
            GetPtNotifications_srz = GetPtNotificationsSerializer(GetPtNotifications, many=True)

            content = {
                "status":True, 
                "username":CurrentUser.username, 
                "notifications":GetPtNotifications_srz.data
                }
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



#PROFILE~IMAGE~UPDATE
@authentication_classes((TokenAuthentication,))
class ProfileImageUpload(APIView):
    parser_classes = (MultiPartParser, JSONParser,)
    
    permission_classes = [
       permissions.IsAuthenticated  
   ]

    @staticmethod
    def post(request):
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            file = request.data.get('profile_pic')

            upload_data = cloudinary.uploader.upload(file)
            
            GetUser.profile_pic = upload_data['url'][50:]
            GetUser.save()

            content = {"status":True, "username":GetUser.username, "detials":"Image Updated", "data": upload_data}
            return Response(content, status=status.HTTP_200_OK)

        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
#THIS~FUNCTION~ONLY~UPDATE~[USERNAME, EMAIL, MOBILE]
def InfoUpdate(request):
    if request.method == 'PUT':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            
            InfoUpdate_srz = InfoUpdateSerializer(GetUser, data=request.data)
            if InfoUpdate_srz.is_valid(raise_exception=True):
                InfoUpdate_srz.save()

                content = {"status":True, "username":GetUser.username, "detials":"Information Updated"}
                return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def PasswordUpdate(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            CurrentPass = request.data['current password']
            NewPass     = request.data['new password']
            ConfirmPass = request.data['confirm password']

            if CurrentPass == GetUser.password:
                if NewPass == ConfirmPass:
                    GetUser.password = NewPass
                    GetUser.save()
                    
                    content = {"status":True, "username":GetUser.username, "details":"Password Updated"}
                    return Response(content, status=status.HTTP_201_CREATED)

                else:
                    content = {"status":False, "username":GetUser.username, "details":"Passwords Didn't Match"}
                    return Response(content, status=status.HTTP_403_FORBIDDEN) 

            else:
                content = {"status":False, "username":GetUser.username, "details":"Current Password uncorrect"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST) 
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def PtAddressUpdate(request):
    if request.method == 'PUT':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            GetPatient = Patients.objects.get(user=GetUser.id)

            PtAddressUpdate_srz = PtAddressUpdateSerializer(GetPatient, data=request.data)
            if PtAddressUpdate_srz.is_valid(raise_exception=True):
                PtAddressUpdate_srz.save()

                content = {"status":True, "username":GetUser.username, "detials":"Address Updated"}
                return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def PtSpecialInfoUpdate(request):
    if request.method == 'PUT':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            GetPatient = Patients.objects.get(user=GetUser.id)

            Dateofbirth = request.data['dateofbirth']
            Blood       = request.data['blood']
            Heigh       = request.data['heigh']
            Weight      = request.data['weight']

            PtSpecialInfoUpdate_srz = PtSpecialInfoUpdateSerializer(GetPatient, data=request.data)
            if PtSpecialInfoUpdate_srz.is_valid(raise_exception=True):
                PtSpecialInfoUpdate_srz.save()

                content = {"status":True, "username":GetUser.username, "detials":"Info Updated"}
                return Response(content, status=status.HTTP_201_CREATED)
  
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def DrSpecialInfoUpdate(request):
    if request.method == 'PUT':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            GetDoctor = Doctors.objects.get(user=GetUser.id)

            Dateofbirth = request.data['dateofbirth']
            Info        = request.data['info']
            Specialize  = request.data['specialize']
            Price       = request.data['price']

            DrSpecialInfoUpdate_srz = DrSpecialInfoUpdateSerializer(GetDoctor, data=request.data)
            if DrSpecialInfoUpdate_srz.is_valid(raise_exception=True):
                DrSpecialInfoUpdate_srz.save()

                content = {"status":True, "username":GetUser.username, "detials":"Info Updated"}
                return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)
