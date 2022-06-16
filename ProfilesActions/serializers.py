from rest_framework import serializers

from Users.models import Doctors, Patients, CustomUser
from DoctorActions.models import Clinics
from .models import *







class PtProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ['gender','dateofbirth','age','address','city','district','blood','heigh','weight' ]


class InfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','mobile']


class PtAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ['city','district','address']


class PtSpecialInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ['dateofbirth','blood','heigh','weight']

class DrSpecialInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['dateofbirth','specialize','price','info','accept_insurance','insurance_company1','insurance_company2','insurance_company3']


class GetDrNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['message']

class GetPtNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['message']


class DoctorClinicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinics
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'

