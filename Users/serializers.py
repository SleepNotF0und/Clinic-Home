from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.response import Response
from rest_framework import status

from .models import *

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _






class DoctorsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['user','specialize','accept_insurance','insurance_company1','insurance_company2','insurance_company3']


class AllTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = '__all__'



class DoctorCreateSerializer(serializers.ModelSerializer):
    info = serializers.CharField(max_length=100, required=True)
    gender = serializers.CharField(max_length=6,required=True)
    dateofbirth = serializers.CharField(max_length=10, required=True)
    accept_insurance = serializers.BooleanField(default=False, required=False, allow_null=True)
    insurance_company1 = serializers.CharField(max_length=100, required=False, allow_blank=True)
    insurance_company2 = serializers.CharField(max_length=100, required=False, allow_blank=True)
    insurance_company3 = serializers.CharField(max_length=100, required=False, allow_blank=True)
    specialize = serializers.CharField(max_length=30, required=True)
    price = serializers.CharField(max_length=10, required=True)
    #image in profile update

    class Meta:
        model = CustomUser
        fields = ['username','password','mobile','info','gender','dateofbirth','accept_insurance','insurance_company1','insurance_company2','insurance_company3','specialize','price']

    def save(self):
        CurrentUser = self.context['request'].user

        CurrentUser.username = self.validated_data['username']
        CurrentUser.password = self.validated_data['password']
        CurrentUser.mobile = self.validated_data['mobile']
        CurrentUser.is_doctor = True
        CurrentUser.save()

        NewDoctor = Doctors(
            user=CurrentUser, 
            info=self.validated_data['info'], 
            gender=self.validated_data['gender'],  
            dateofbirth=self.validated_data['dateofbirth'],
            accept_insurance=self.validated_data['accept_insurance'],
            insurance_company1=self.validated_data['insurance_company1'],
            insurance_company2=self.validated_data['insurance_company2'],
            insurance_company3=self.validated_data['insurance_company3'],
            specialize=self.validated_data['specialize'], 
            price=self.validated_data['price']
        )
        NewDoctor.save()

        


class PatientCreateSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(max_length=6,required=True)
    city = serializers.CharField(max_length=10, required=True)
    dateofbirth = serializers.CharField(max_length=10, required=True)
    age = serializers.CharField(max_length=5, required=True)
    blood = serializers.CharField(max_length=10, required=True)
    heigh = serializers.CharField(max_length=10, required=True)
    weight = serializers.CharField(max_length=10, required=True)
    #image in profile update

    class Meta:
        model = CustomUser
        fields = ['username','password','mobile','gender','city','dateofbirth','age','blood','heigh','weight']

    def save(self):
        CurrentUser = self.context['request'].user

        CurrentUser.username = self.validated_data['username']
        CurrentUser.password = self.validated_data['password']
        CurrentUser.mobile = self.validated_data['mobile']
        CurrentUser.is_patient = True
        CurrentUser.save()

        NewPatient = Patients(
            user=CurrentUser,  
            gender=self.validated_data['gender'], 
            city=self.validated_data['city'],
            dateofbirth=self.validated_data['dateofbirth'],
            age=self.validated_data['age'], 
            blood=self.validated_data['blood'],
            heigh=self.validated_data['heigh'],
            weight=self.validated_data['weight']
        )
        NewPatient.save()



