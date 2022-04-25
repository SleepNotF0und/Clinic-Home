from rest_framework import serializers

from Users.models import Doctors, Patients, CustomUser
from .models import Reservations, Comments




class SearchByNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'is_doctor', 'username', 'profile_pic']


class SearchByCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['user', 'city', 'district', 'address', 'specialize']


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = '__all__'


class DoctorCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['user','comment']

class GetPtReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['doctor','createdate','accepted','opptdate']