from rest_framework import serializers

from Users.models import Doctors, Patients, CustomUser
from PatientActions.models import Reservations, Comments



class GetDrReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['user','createdate','accepted']