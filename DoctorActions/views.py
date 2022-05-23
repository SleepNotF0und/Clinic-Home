from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, get_user_model

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

import cloudinary.uploader

from Users.models import Doctors, Patients
from PatientActions.models import Reservations, Comments
from ProfilesActions.models import Notifications
from .models import *

from .serializers import *







@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def AcceptReservation(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            if GetUser.is_doctor == True:
                
                PatientId = request.data['patient']

                try:
                    GetPatientUser = get_user_model().objects.get(id=PatientId)
                    GetPatient = Patients.objects.get(user=GetPatientUser.id)
                    
                    try:
                        GetReservation = Reservations.objects.get(user=GetPatientUser.id)
                        GetReservation.accepted = True
                        GetReservation.save()
                        
                        #FIRE~A~NOTIFICATION~TO~THE~PATIENT
                        Notifications.objects.create(currentuser=CurrentUser, patient=GetPatient, message=CurrentUser.username+" Accepted your Reservation & doctor will call you to confirm the reservation")

                        content = {
                            "status":True, 
                            "details":"Reservation Accepted", 
                            "Doctor":GetUser.username, 
                            "Patient":GetPatientUser.username
                            }
                        return Response(content, status=status.HTTP_201_CREATED)
                    
                    except Reservations.DoesNotExist:
                        content = {"status":False, "details":"this Patient doesn't have reservation with you"}     
                        return Response(content, status=status.HTTP_404_NOT_FOUND)
                
                except get_user_model().DoesNotExist:
                    content = {"status":False, "details":"Patient not found"}     
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

            else:
                content = {"status":False, "details":"You are not doctor !"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def RefuseReservation(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            if GetUser.is_doctor == True:
                
                PatientId = request.data['patient']

                try:
                    GetPatientUser = get_user_model().objects.get(id=PatientId)
                    GetPatient = Patients.objects.get(user=GetPatientUser.id)
                    
                    try:
                        GetReservation = Reservations.objects.get(user=GetPatientUser.id)
                        GetReservation.accepted = False
                        GetReservation.save()
                        
                        #FIRE~A~NOTIFICATION~TO~THE~PATIENT
                        Notifications.objects.create(currentuser=CurrentUser, patient=GetPatient, message=CurrentUser.username+" Cancelled your Reservation")

                        content = {
                            "status":True, 
                            "details":"Reservation Refused", 
                            "Doctor":GetUser.username, 
                            "Patient":GetPatientUser.username
                            }
                        return Response(content, status=status.HTTP_201_CREATED)

                    except Reservations.DoesNotExist:
                        content = {"status":False, "details":"this Patient doesn't have reservation with you"}     
                        return Response(content, status=status.HTTP_404_NOT_FOUND)
                
                except get_user_model().DoesNotExist:
                    content = {"status":False, "details":"Patient not found"}     
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

            else:
                content = {"status":False, "details":"You are not doctor !"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def ViewAppointments(request):
    if request.method == 'GET':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            GetDoctor = Doctors.objects.get(user=GetUser.id)

            GetDrReservations = Reservations.objects.filter(doctor=GetDoctor)
            GetDrReservations_srz = GetDrReservationsSerializer(GetDrReservations, many=True)

            data = { 'appointments': [] }
            for ele in GetDrReservations_srz.data:
                GetPatientUser = CustomUser.objects.get(email=ele['user'])          
                GetImage = GetPatientUser.profile_pic

                if GetImage and hasattr(GetImage, 'url'):
                    CurrentImage = GetImage.url
                else:
                    CurrentImage = "User has No Profile Pic"
                
                if GetUser:
                    ele['user'] = GetPatientUser.username
                    ele['profile_link'] = 'https://clinichome.herokuapp.com/api/action/dr/patients/'+str(GetPatientUser.id)+'/'
                    data['appointments'].append(ele)


            content = {
                "status":True, 
                "doctor":GetUser.username,
                "data":data
                }
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def CreateClinic(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            if GetUser.is_doctor == True:
                
                ClinicName = request.data['clinicname']
                WorkHours = request.data['workhours']
                
                City = request.data['city']
                District = request.data['district']
                Address = request.data['address']
                
                #CREATE~CLINIC
                Clinics.objects.create(
                    user=CurrentUser, 
                    clinicname=ClinicName, 
                    workhours=WorkHours, 
                    city=City, 
                    district=District, 
                    address=Address
                    )
            
                content = {
                    "status":True, 
                    "details":"Clinic Created", 
                    "Doctor":CurrentUser.username, 
                    "clinic name":ClinicName
                    }
                return Response(content, status=status.HTTP_201_CREATED)                 

            else:
                content = {"status":False, "details":"You are not doctor !"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['PUT'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def UpdateClinic(request):
    if request.method == 'PUT':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            if GetUser.is_doctor == True:

                ClinicId = request.data['clinic']
                GetClinic = Clinics.objects.get(user=GetUser, id=ClinicId)

                ClinicUpdate_srz = ClinicUpdateSerializer(GetClinic, data=request.data)                
                if ClinicUpdate_srz.is_valid(raise_exception=True):
                    ClinicUpdate_srz.save()
            
                content = {"status":True, "details":"Clinic Updated"}
                return Response(content, status=status.HTTP_201_CREATED)
               
            else:
                content = {"status":False, "details":"You are not doctor !"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




#CLINIC~IMAGE~UPLOAD
@authentication_classes((TokenAuthentication,))
class ClinicImageUpload(APIView):
    parser_classes = (MultiPartParser, JSONParser,)
    
    permission_classes = [
       permissions.IsAuthenticated  
   ]

    @staticmethod
    def post(request):
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            if GetUser.is_doctor == True:

                ClinicId = request.data['clinic']

                try:
                    GetClinic = Clinics.objects.get(user=GetUser, id=ClinicId)

                    file = request.data.get('clinic_image')

                    upload_data = cloudinary.uploader.upload(file)
                    
                    GetClinic.clinic_image = upload_data['url'][50:]
                    GetClinic.save()

                    content = {"status":True, "username":GetUser.username, "details":"Clinic Image Updated", "data": upload_data}
                    return Response(content, status=status.HTTP_200_OK)

                except Clinics.DoesNotExist:
                    content = {"status":False, "username":GetUser.username, "details":"Clinic Doesn't Exist Or you don't belong this clinic"}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
               
            else:
                content = {"status":False, "details":"You are not doctor !"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)





@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def ViewPatientProfile(request, id):
    if request.method == 'GET':
        try:
            GetUser = get_user_model().objects.get(id=id)
            GetImage = GetUser.profile_pic

            GetPatient = Patients.objects.get(user=GetUser.id)

            if GetImage and hasattr(GetImage, 'url'):
                UserImage = GetImage.url
            else:
                UserImage = "User has No Profile Pic"

            content = {
                "status":True,
                "Username":GetUser.username, 
                "ImageURL":UserImage,
                "Mobile":GetUser.mobile, 
                "gender":GetPatient.gender,
                "dateofbirth":GetPatient.dateofbirth,
                "age":GetPatient.age,
                "blood":GetPatient.blood,
                "heigh":GetPatient.heigh,
                "weight":GetPatient.weight,
                "city":GetPatient.city
            }
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Patient not found Or Not Doctor Id"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)
