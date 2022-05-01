from django.http import HttpResponse, JsonResponse

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, get_user_model

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.generics import ListAPIView

from rest_framework.filters import SearchFilter

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

from Users.models import Doctors, Patients
from ProfilesActions.models import Notifications
from .models import Reservations, Comments

from .serializers import *






class SearchByName(ListAPIView):
    queryset  = CustomUser.objects.all()
    serializer_class = SearchByNameSerializer
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_backends = [ DjangoFilterBackend, SearchFilter ]
    search_fields = [ 'username' ]



class SearchByCity(ListAPIView):
    queryset  = Doctors.objects.all()
    serializer_class = SearchByCitySerializer
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_backends = [ DjangoFilterBackend, SearchFilter ]
    search_fields = [ 'city' ]



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def ViewDoctorProfile(request, id):
    if request.method == 'GET':
        try:
            GetUser = get_user_model().objects.get(id=id)
            GetImage = GetUser.profile_pic

            GetDoctor = Doctors.objects.get(user=GetUser.id)

            if GetImage and hasattr(GetImage, 'url'):
                UserImage = GetImage.url
            else:
                UserImage = "User has No Profile Pic"

            DoctorComments = Comments.objects.filter(doctor=GetDoctor.id)
            DoctorComments_srz = DoctorCommentsSerializer(DoctorComments, many=True)

            content = {
                "status":True,
                "Username":GetUser.username, 
                "ImageURL":UserImage, 
                "specialize":GetDoctor.specialize,
                "price":GetDoctor.price,
                "info":GetDoctor.info,
                "city":GetDoctor.city,
                "district":GetDoctor.district,
                "address":GetDoctor.address,
                "comments":DoctorComments_srz.data
            }
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User Not Found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def Reserve(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            if GetUser.is_patient == True:
                
                DoctorName = request.data['doctor']

                GetDoctorUser = get_user_model().objects.get(username=DoctorName)
                GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)
                
                Reservations.objects.create(user=CurrentUser, doctor=GetDoctorId)
                
                #FIRE~A~NOTIFICATION~TO~THE~DOCTOR
                Notifications.objects.create(currentuser=CurrentUser, doctor=GetDoctorId, message=CurrentUser.username+" Request an oppointment with you")

                content = {
                    "status":True, 
                    "details":"Reservation Created Thank You", 
                    "doctor":GetDoctorUser.username,
                    "price":GetDoctorUser.price,
                    "address":GetDoctorUser.address
                    }
                return Response(content, status=status.HTTP_201_CREATED)

            else:
                content = {"status":False, "details":"You are not patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User Not Found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def DeleteReserve(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            if GetUser.is_patient == True:
                
                DoctorName = request.data['doctor']

                GetDoctorUser = get_user_model().objects.get(username=DoctorName)
                GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)
                
                try:
                    Reservations.objects.get(user=CurrentUser, doctor=GetDoctorId).delete()
                    
                    #FIRE~A~NOTIFICATION~TO~THE~DOCTOR
                    Notifications.objects.create(currentuser=CurrentUser, doctor=GetDoctorId, message=CurrentUser.username+" Cancelled his oppointment with you")

                    content = {
                        "status":True, 
                        "details":"Reservation Deleted", 
                        "Patient":GetUser.username, 
                        "doctor":GetDoctorUser.username
                        }
                    return Response(content, status=status.HTTP_201_CREATED)

                except Reservations.DoesNotExist:
                    content = {
                        "status":False, 
                        "details":"You don't have a Reservation with that doctor", 
                        "Patient":GetUser.username, 
                        "doctor":GetDoctorUser.username
                        }
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

            else:
                content = {"status":False, "details":"You are not Patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User Not Found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def Comment(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            if GetUser.is_patient == True:
                
                Comment = request.data['comment']
                DoctorName = request.data['doctor']

                GetDoctorUser = get_user_model().objects.get(username=DoctorName)
                GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)
                
                Comments.objects.create(user=CurrentUser, doctor=GetDoctorId, comment=Comment)

                #FIRE~A~NOTIFICATION~TO~THE~DOCTOR
                Notifications.objects.create(currentuser=CurrentUser, doctor=GetDoctorId, message=CurrentUser.username +"Commented: "+ Comment)

                content = {
                    "status":True, 
                    "details":"Commnet Created", 
                    "Patient":GetUser.username, 
                    "doctor":GetDoctorUser.username,
                    "comment":Comment
                    }
                return Response(content, status=status.HTTP_201_CREATED)

            else:
                content = {"status":False, "details":"You are not patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User Not Found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def DeleteComment(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)

            if GetUser.is_patient == True:
                
                Comment = request.data['comment']
                DoctorName = request.data['doctor']

                GetDoctorUser = get_user_model().objects.get(username=DoctorName)
                GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)
                
                try:
                    Comments.objects.get(user=CurrentUser, doctor=GetDoctorId, comment=Comment).delete()
                    
                    content = {
                        "status":True, 
                        "details":"Comment Deleted", 
                        "Patient":GetUser.username, 
                        "doctor":GetDoctorUser.username
                        }
                    return Response(content, status=status.HTTP_201_CREATED)

                except Comments.DoesNotExist:
                    
                    content = {
                        "status":False, 
                        "details":"Comment Not Found", 
                        "Patient":GetUser.username, 
                        "doctor":GetDoctorUser.username
                        }
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

            else:
                content = {"status":False, "details":"You are not patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"User Not Found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def ViewReservations(request):
    if request.method == 'GET':
        CurrentUser = request.user

        GetPtReservations = Reservations.objects.filter(user=CurrentUser)
        GetPtReservations_srz = GetPtReservationsSerializer(GetPtReservations, many=True)

        content = {
            "status":True, 
            "username":CurrentUser.username, 
            "Reservations":GetPtReservations_srz.data,
            }
        return Response(content, status=status.HTTP_200_OK)







@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
#DEBUG
def GET_Reservations(request):
    if request.method == 'GET':
        Reservations_db = Reservations.objects.all()
        Reservations_srz = ReservationsSerializer(Reservations_db, many=True)

        content = {"status":True, "data":Reservations_srz.data}     
        return Response(content, status=status.HTTP_404_NOT_FOUND)

