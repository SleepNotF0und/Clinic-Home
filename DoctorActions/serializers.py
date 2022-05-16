from rest_framework import serializers

from Users.models import Doctors, Patients, CustomUser
from PatientActions.models import Reservations, Comments
from .models import Clinics




class GetDrReservationsSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    clinic = serializers.StringRelatedField()

    class Meta:
        model = Reservations
        fields = ['user','clinic','createdate','opptdate','accepted']


class ClinicUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinics
        fields = ['clinicname','workhours','city','district','address','clinic_image']
