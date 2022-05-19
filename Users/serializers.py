from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.response import Response
from rest_framework import status

from . import facebook
from .register import register_social_user
from .models import *

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _






class DoctorsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = ['user','specialize']


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
    specialize = serializers.CharField(max_length=30, required=True)
    price = serializers.CharField(max_length=10, required=True)
    #image in profile update

    class Meta:
        model = CustomUser
        fields = ['username','password','info','gender','dateofbirth','specialize','price']

    def save(self):
        CurrentUser = self.context['request'].user

        CurrentUser.username = self.validated_data['username']
        CurrentUser.password = self.validated_data['password']
        CurrentUser.is_doctor = True
        CurrentUser.save()

        NewDoctor = Doctors(
            user=CurrentUser, 
            info=self.validated_data['info'], 
            gender=self.validated_data['gender'],  
            dateofbirth=self.validated_data['dateofbirth'], 
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
        fields = ['username','password','gender','city','dateofbirth','age','blood','heigh','weight']

    def save(self):
        CurrentUser = self.context['request'].user

        CurrentUser.username = self.validated_data['username']
        CurrentUser.password = self.validated_data['password']
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




class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)

        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            return register_social_user(
                provider=provider,
                user_id=user_id,
                email=email,
                name=name
            )
        except Exception as identifier:

            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )


