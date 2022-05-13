from rest_framework import serializers

from Users.models import Doctors, Patients, CustomUser
from DoctorActions.models import Clinics
from .models import Reservations, Comments




class SearchByNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'is_doctor', 'is_patient', 'username', 'profile_pic']


class SearchClinicByCitySerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Clinics
        fields = '__all__'



class DoctorCommentsSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Comments
        fields = ['user','comment']


class DoctorClinicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinics
        fields = '__all__'


class GetPtReservationsSerializer(serializers.ModelSerializer):

    doctor = serializers.StringRelatedField()
    clinic = serializers.StringRelatedField()

    class Meta:
        model = Reservations
        fields = ['doctor','clinic','createdate','accepted','opptdate']


class ViewClinicSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    
    class Meta:
        model = Clinics
        fields = '__all__'