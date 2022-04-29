from rest_framework import serializers

from Users.models import Doctors, Patients, CustomUser
from .models import Notifications





class InfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','mobile']


class PtAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ['city','district','address']

class DrAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['city','district','address']


class PtSpecialInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patients
        fields = ['dateofbirth','blood','heigh','weight']

class DrSpecialInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['dateofbirth','specialize','price','info']


class GetDrNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['message']

class GetPtNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['message']

