from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status
from rest_framework import generics

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

import cloudinary.uploader

from Users.models import Doctors, Patients
from PatientActions.models import Reservations
from DoctorActions.models import Clinics
from .models import *

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
        "mobile":CurrentUser.mobile,
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

            DoctorClinics = Clinics.objects.filter(user=GetUser.id)
            DoctorClinics_srz = DoctorClinicsSerializer(DoctorClinics, many=True)

            content = {
                "status":True, 
                "username":CurrentUser.username, 
                "imageURL":CurrentImage, 
                "info":GetDoctor.info,
                "gender":GetDoctor.gender,
                "date of birth":GetDoctor.dateofbirth,
                "accept_insurance":GetDoctor.accept_insurance,
                "insurance_company1":GetDoctor.insurance_company1,
                "insurance_company2":GetDoctor.insurance_company2,
                "insurance_company3":GetDoctor.insurance_company3,
                "specialize":GetDoctor.specialize, 
                "price":GetDoctor.price,
                "clinics":DoctorClinics_srz.data
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

            DrSpecialInfoUpdate_srz = DrSpecialInfoUpdateSerializer(GetDoctor, data=request.data)
            if DrSpecialInfoUpdate_srz.is_valid(raise_exception=True):
                DrSpecialInfoUpdate_srz.save()

                content = {"status":True, "username":GetUser.username, "detials":"Info Updated"}
                return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



#===================================
#~~~~~~~~~CHAT~APP~METHODS~~~~~~~~~~
#===================================

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def PtSendMessage(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            send_to = request.data['send_to']
            message = request.data['message']

            receiver = get_user_model().objects.get(id=send_to)

            #CREATE~CHAT
            if not Chat.objects.filter(patient=GetUser, doctor=receiver):
                Chat.objects.create(patient=GetUser, doctor=receiver)
                      
            GetChat = Chat.objects.get(patient=GetUser, doctor=receiver)            
            Messages.objects.create(chat_id=GetChat, message=message, sender=GetUser)
            
            content = {"status":True, "sender":GetUser.username, "details":"Message Sent", "message":message}
            return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"doctor account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def DrSendMessage(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            send_to = request.data['send_to']
            message = request.data['message']

            receiver = get_user_model().objects.get(id=send_to)

            #CREATE~CHAT
            if not Chat.objects.filter(doctor=GetUser, patient=receiver):
                Chat.objects.create(doctor=GetUser, patient=receiver)
                      
            GetChat = Chat.objects.get(doctor=GetUser, patient=receiver)            
            Messages.objects.create(chat_id=GetChat, message=message, sender=GetUser)
            
            content = {"status":True, "sender":GetUser.username, "details":"Message Sent", "message":message}
            return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"patient account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def PtChatList(request):
    if request.method == 'GET':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            GetUserChats = Chat.objects.filter(patient=GetUser)
            chats_srz = ChatSerializer(GetUserChats, many=True)

            data = { 'chats': [] }

            for ele in chats_srz.data:
                Get_doctor = CustomUser.objects.get(pk=ele['doctor'])

                Get_doctor_Image = Get_doctor.profile_pic

                if Get_doctor_Image and hasattr(Get_doctor_Image, 'url'):
                    DoctorImage = Get_doctor_Image.url
                else:
                    DoctorImage = "User has No Profile Pic"         
                
                if Get_doctor:
                    ele['doctor_name'] = Get_doctor.username
                    ele['doctor_image'] = DoctorImage
                    data['chats'].append(ele)


            content = {"status":True, "username":GetUser.username, "mychats":chats_srz.data}
            return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def DrChatList(request):
    if request.method == 'GET':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            GetUserChats = Chat.objects.filter(doctor=GetUser)
            chats_srz = ChatSerializer(GetUserChats, many=True)

            data = { 'chats': [] }

            for ele in chats_srz.data:
                Get_patient = CustomUser.objects.get(pk=ele['patient'])

                Get_patient_Image = Get_patient.profile_pic

                if Get_patient_Image and hasattr(Get_patient_Image, 'url'):
                    PatientImage = Get_patient_Image.url
                else:
                    PatientImage = "User has No Profile Pic"         
                
                if Get_patient:
                    ele['patient_name'] = Get_patient.username
                    ele['patient_image'] = PatientImage
                    data['chats'].append(ele)


            content = {"status":True, "username":GetUser.username, "mychats":chats_srz.data}
            return Response(content, status=status.HTTP_201_CREATED)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def PtChatWith(request):
    if request.method == 'GET':
        CurrentUser = request.user
        GetUser = get_user_model().objects.get(id=CurrentUser.id)

        with_user = request.GET.get('with', '')
        

        GetUserChat = Chat.objects.get(patient=GetUser, doctor=with_user)
        GetChatMessages = Messages.objects.filter(chat_id=GetUserChat)

        messages_srz = MessagesSerializer(GetChatMessages, many=True)
        
        data = { 'chat': [] }

        for ele in messages_srz.data:
            Get_sender = CustomUser.objects.get(pk=ele['sender'])

            GetSender_Image = Get_sender.profile_pic

            if GetSender_Image and hasattr(GetSender_Image, 'url'):
                SenderImage = GetSender_Image.url
            else:
                SenderImage = "User has No Profile Pic"          
            
            if Get_sender:
                ele['sender_username'] = Get_sender.username
                ele['sender_image'] = SenderImage
                data['chat'].append(ele)
             
        content = {"status":True, "details":"success", "mychat":data}
        return Response(content, status=status.HTTP_200_OK)




@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def DrChatWith(request):
    if request.method == 'GET':
        CurrentUser = request.user
        GetUser = get_user_model().objects.get(id=CurrentUser.id)

        with_user = request.GET.get('with', '')
        

        GetUserChat = Chat.objects.get(doctor=GetUser, patient=with_user)
        GetChatMessages = Messages.objects.filter(chat_id=GetUserChat)

        messages_srz = MessagesSerializer(GetChatMessages, many=True)
        
        data = { 'chat': [] }

        for ele in messages_srz.data:
            Get_sender = CustomUser.objects.get(pk=ele['sender'])

            GetSender_Image = Get_sender.profile_pic

            if GetSender_Image and hasattr(GetSender_Image, 'url'):
                SenderImage = GetSender_Image.url
            else:
                SenderImage = "User has No Profile Pic"          
            
            if Get_sender:
                ele['sender_username'] = Get_sender.username
                ele['sender_image'] = SenderImage
                data['chat'].append(ele)
             
        content = {"status":True, "details":"success", "mychat":data}
        return Response(content, status=status.HTTP_200_OK)