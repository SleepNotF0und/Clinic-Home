from django.http import HttpResponse, JsonResponse

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, get_user_model

from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from Users.models import Doctors, Patients
from PatientActions.models import Reservations, Comments
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
                
                PatientName = request.data['patient']
                OppointmentDate = request.data['time']

                GetPatientUser = get_user_model().objects.get(username=PatientName)
                
                GetReservation = Reservations.objects.get(user=GetPatientUser.id)
                GetReservation.accepted = True
                GetReservation.opptdate = OppointmentDate
                GetReservation.save()
                
                content = {"status":True, "details":"Reservation Accepted", "Doctor":GetUser.username, "Patient":GetPatientUser.username}
                return Response(content, status=status.HTTP_201_CREATED)

            else:
                content = {"status":False, "details":"You are not doctor !"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User Not Found"}     
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
                
                PatientName = request.data['patient']
                GetPatientUser = get_user_model().objects.get(username=PatientName)
                
                GetReservation = Reservations.objects.get(user=GetPatientUser.id)
                GetReservation.accepted = False
                GetReservation.save()
                
                content = {"status":True, "details":"Reservation Refused", "Doctor":GetUser.username, "Patient":GetPatientUser.username}
                return Response(content, status=status.HTTP_201_CREATED)

            else:
                content = {"status":False, "details":"You are not doctor !"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User Not Found"}     
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
            GetImage = CurrentUser.profile_pic

            GetDoctor = Doctors.objects.get(user=GetUser.id)

            GetDrReservations = Reservations.objects.filter(doctor=GetDoctor)
            GetDrReservations_srz = GetDrReservationsSerializer(GetDrReservations, many=True)

            content = {
                "status":True, 
                "username":GetUser.username,
                "appointments":GetDrReservations_srz.data
                }
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User Not Found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)