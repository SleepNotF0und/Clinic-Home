from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Max
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
from DoctorActions.models import Clinics
from .models import *

from .serializers import *






class SearchByName(ListAPIView):
    queryset  = CustomUser.objects.all()
    serializer_class = SearchByNameSerializer
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_backends = [ DjangoFilterBackend, SearchFilter ]
    search_fields = [ 'username' ]


class SearchClinicByCity(ListAPIView):
    queryset  = Clinics.objects.all()
    serializer_class = SearchClinicByCitySerializer
    
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

            #CHECK~IF~DOCTOR~HAVE~PROFILE~PIC
            if GetImage and hasattr(GetImage, 'url'):
                UserImage = GetImage.url
            else:
                UserImage = "User has No Profile Pic"

            #GET~DOCTOR~THANKS
            try:
                GetThanks = Thanks.objects.get(doctor=GetDoctor.id)
                GetDoctorThanks = GetThanks.thanks
            except Thanks.DoesNotExist:
                GetDoctorThanks = 0

            #GET~DOCTORS~COMMENTS
            DoctorComments = Comments.objects.filter(doctor=GetDoctor.id)
            DoctorComments_srz = DoctorCommentsSerializer(DoctorComments, many=True)

            data = { 'comments': [] }
            for ele in DoctorComments_srz.data:
                GetPatientUser = CustomUser.objects.get(id=ele['user'])          
                GetImage = GetPatientUser.profile_pic

                if GetImage and hasattr(GetImage, 'url'):
                    CurrentImage = GetImage.url
                else:
                    CurrentImage = "User has No Profile Pic"
                
                if GetUser:
                    ele['user'] = GetPatientUser.username
                    ele['profile_pic'] = CurrentImage
                    data['comments'].append(ele)

            content = {
                "status":True,
                "doctor":GetUser.username, 
                "ImageURL":UserImage,
                "info":GetDoctor.info, 
                "specialize":GetDoctor.specialize,
                "price":GetDoctor.price,
                "thanks":GetDoctorThanks,
                "patients comments":data
            }
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"doctor not found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def ViewDoctorClinics(request, id):
    if request.method == 'GET':
        try:
            GetUser = get_user_model().objects.get(id=id)

            DoctorClinics = Clinics.objects.filter(user=GetUser.id)
            DoctorClinics_srz = DoctorClinicsSerializer(DoctorClinics, many=True)
            DoctorCities_srz = DoctorCitiesSerializer(DoctorClinics, many=True)

            content = {
                "status":True,
                "doctor":GetUser.username, 
                "available cities":DoctorCities_srz.data,
                "clinics":DoctorClinics_srz.data
            }
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Clinic not found"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def ViewClinic(request, id):
    if request.method == 'GET':
        try:
            GetClinic = Clinics.objects.filter(id=id)
            GetClinic_srz = ViewClinicSerializer(GetClinic, many=True)

            data = { 'data': [] }
            for ele in GetClinic_srz.data:
                GetDoctorUser = CustomUser.objects.get(id=ele['user'])          
                
                if GetDoctorUser:
                    ele['user'] = GetDoctorUser.username
                    data['data'].append(ele)
        
            content = {"status":True, "clinic":data}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        except Clinics.DoesNotExist:
            content = {"status":False, "details":"Clinic doesn't exist"}     
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
                
                ClinicId = request.data['clinic']
                DoctorId = request.data['doctor']
                SetTime = request.data['opptdate']

                GetDoctorUser = get_user_model().objects.get(id=DoctorId)
                GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)
                
                #CHECK~IF~PATIENT~HAVE~ALREADY~RESERVE~WITH~THAT~DOCTOR
                if not Reservations.objects.filter(user=CurrentUser, doctor=GetDoctorId):

                    try:
                        #GET~DOCTOR'S~CLINIC
                        GetClinic = Clinics.objects.get(user=GetDoctorUser, id=ClinicId)
                    except Clinics.DoesNotExist:
                        content = {"status":False, "details":"the doctor doesn't work in this clinic !"}     
                        return Response(content, status=status.HTTP_400_BAD_REQUEST) 

                    #CHECK~IF~PATIENT~HAVE~MOBILE
                    if GetUser.mobile != None:

                        #CREATE~RESERVATION
                        Reservations.objects.create(user=CurrentUser, doctor=GetDoctorId, opptdate=SetTime, clinic=GetClinic)
                    
                        #FIRE~A~NOTIFICATION~TO~THE~DOCTOR
                        Notifications.objects.create(
                            currentuser=CurrentUser, 
                            doctor=GetDoctorId, 
                            message=CurrentUser.username+" Request an oppointment with you in clinic "+GetClinic.clinicname
                            )

                        content = {
                            "status":True, 
                            "details":"Reservation Created Thank You", 
                            "doctor":GetDoctorUser.username,
                            "price":GetDoctorId.price,
                            "clinic name":GetClinic.clinicname,
                            "clinic city":GetClinic.city,
                            "clinic address":GetClinic.address,
                            "requested time":SetTime
                            }
                        return Response(content, status=status.HTTP_201_CREATED)

                    else:
                        content = {"status":False, "details":"Please fill your mobile in profile settings, so doctor can confirm the reservation with you"}     
                        return Response(content, status=status.HTTP_400_BAD_REQUEST) 
                
                else:
                    content = {"status":False, "details":"You already Have Reservation with that doctor !"}     
                    return Response(content, status=status.HTTP_403_FORBIDDEN)                    

            else:
                content = {"status":False, "details":"You are not patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
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
                
                DoctorId = request.data['doctor']

                GetDoctorUser = get_user_model().objects.get(id=DoctorId)
                GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)
                
                try:
                    Reservations.objects.get(user=CurrentUser, doctor=GetDoctorId).delete()
                    
                    #FIRE~A~NOTIFICATION~TO~THE~DOCTOR
                    Notifications.objects.create(
                        currentuser=CurrentUser, 
                        doctor=GetDoctorId, 
                        message=CurrentUser.username+" Cancelled his oppointment with you"
                        )

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
            content = {"status":False, "details":"Your account doesn't exist"}     
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
                
                DoctorId = request.data['doctor']
                Comment = request.data['comment']

                GetDoctorUser = get_user_model().objects.get(id=DoctorId)
                GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)
                
                #CHECK~IF~COMMENT~ALREADY~EXISTS
                if not Comments.objects.filter(user=CurrentUser, doctor=GetDoctorId):
                    Comments.objects.create(user=CurrentUser, doctor=GetDoctorId, comment=Comment)

                    #FIRE~A~NOTIFICATION~TO~THE~DOCTOR
                    Notifications.objects.create(
                        currentuser=CurrentUser, 
                        doctor=GetDoctorId, 
                        message=CurrentUser.username +" Commented: "+ Comment
                        )

                    content = {
                        "status":True, 
                        "details":"Commnet Created", 
                        "Patient":GetUser.username, 
                        "doctor":GetDoctorUser.username,
                        "comment":Comment
                        }
                    return Response(content, status=status.HTTP_201_CREATED)

                else:
                    content = {"status":False, "details":"You already added comment review for that doctor"}     
                    return Response(content, status=status.HTTP_403_FORBIDDEN)

            else:
                content = {"status":False, "details":"You are not patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
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
                
                DoctorId = request.data['doctor']

                GetDoctorUser = get_user_model().objects.get(id=DoctorId)
                GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)
                
                try:
                    Comments.objects.get(user=CurrentUser, doctor=GetDoctorId).delete()
                    
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
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def MakeThanks(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            if GetUser.is_patient == True:
                
                DoctorId = request.data['doctor']
                
                try:
                    GetDoctorUser = get_user_model().objects.get(id=DoctorId)
                    GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)

                    if not Thanks.objects.filter(user=CurrentUser, doctor=GetDoctorId):
                        Thanks.objects.create(user=CurrentUser, doctor=GetDoctorId, thanks=+1)

                        #FIRE~A~NOTIFICATION~TO~THE~DOCTOR
                        Notifications.objects.create(
                            currentuser=CurrentUser,
                            doctor=GetDoctorId, 
                            message=CurrentUser.username +" Thanked You"
                            )

                        content = {"status":True, "details":"Thanks Added"}
                        return Response(content, status=status.HTTP_201_CREATED)

                    else:
                        content = {"status":False, "details":"You already thanked that doctor"}
                        return Response(content, status=status.HTTP_201_CREATED)       

                except get_user_model().DoesNotExist:                   
                    content = {"status":False, "details":"Doctor not found"}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

            else:
                content = {"status":False, "details":"You are not patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def MakePreview(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            if GetUser.is_patient == True:
                
                DoctorId = request.data['doctor']
                
                try:
                    GetDoctorUser = get_user_model().objects.get(id=DoctorId)
                    GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)

                    if not Previews.objects.filter(user=CurrentUser, doctor=GetDoctorId):
                        Previews.objects.create(user=CurrentUser, doctor=GetDoctorId, preview=+1)

                        #FIRE~A~NOTIFICATION~TO~THE~DOCTOR
                        Notifications.objects.create(
                            currentuser=CurrentUser,
                            doctor=GetDoctorId, 
                            message=CurrentUser.username +" Previewed You"
                            )

                        content = {"status":True, "details":"Preview Added"}
                        return Response(content, status=status.HTTP_201_CREATED)

                    else:
                        content = {"status":False, "details":"You already Previewed that doctor"}
                        return Response(content, status=status.HTTP_201_CREATED)       

                except get_user_model().DoesNotExist:                   
                    content = {"status":False, "details":"Doctor not found"}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

            else:
                content = {"status":False, "details":"You are not patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def UndoThanks(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            if GetUser.is_patient == True:
                
                DoctorId = request.data['doctor']
                
                try:
                    GetDoctorUser = get_user_model().objects.get(id=DoctorId)
                    GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)

                    Thanks.objects.filter(user=CurrentUser, doctor=GetDoctorId).delete()

                    content = {"status":True, "details":"Thanks Deleted"}
                    return Response(content, status=status.HTTP_201_CREATED)

                except get_user_model().DoesNotExist:                   
                    content = {"status":False, "details":"Doctor not found"}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

            else:
                content = {"status":False, "details":"You are not patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def UndoPreview(request):
    if request.method == 'POST':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)
            if GetUser.is_patient == True:
                
                DoctorId = request.data['doctor']
                
                try:
                    GetDoctorUser = get_user_model().objects.get(id=DoctorId)
                    GetDoctorId = Doctors.objects.get(user=GetDoctorUser.id)

                    Previews.objects.filter(user=CurrentUser, doctor=GetDoctorId).delete()

                    content = {"status":True, "details":"Preview Deleted"}
                    return Response(content, status=status.HTTP_201_CREATED)

                except get_user_model().DoesNotExist:                   
                    content = {"status":False, "details":"Doctor not found"}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

            else:
                content = {"status":False, "details":"You are not patient"}     
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
#========================
def TopRated(request):
    if request.method == 'GET':
        CurrentUser = request.user

        try:
            GetUser = get_user_model().objects.get(id=CurrentUser.id)       

            #max_thanks = Thanks.objects.aggregate(Max('thanks'))
            #get_max = Thanks.objects.get(thanks=max_thanks)

            thanks_db = Thanks.objects.all()
            thanks_srz = TopRatedSerializer(thanks_db, many=True)

            data = { 'top thanks': [] }
            for ele in thanks_srz.data:
                
                if ele['thanks'] >= 20:
                    data['top thanks'].append(ele)
                else:
                    pass

            content = {"status":True, "data":data}     
            return Response(content, status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            content = {"status":False, "details":"Your account doesn't exist"}     
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        