from rest_framework import serializers

from Users.models import Doctors, Patients, CustomUser
from DoctorActions.models import Clinics
from .models import *




class SearchByNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'is_doctor', 'is_patient', 'username', 'profile_pic']


class SearchClinicByCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinics
        fields = '__all__'


class DoctorCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['user','comment']


class DoctorClinicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinics
        fields = '__all__'


class DoctorCitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinics
        fields = ['city']


class GetPtReservationsSerializer(serializers.ModelSerializer):

    clinic = serializers.StringRelatedField()

    class Meta:
        model = Reservations
        fields = ['doctor','clinic','createdate','accepted','opptdate']


class ViewClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinics
        fields = '__all__'


class TopRatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['user','specialize','thanks']

