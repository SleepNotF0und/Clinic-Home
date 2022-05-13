from django.db import models
from django.db.models.signals import post_save

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from cloudinary.models import CloudinaryField 

from django.contrib.auth.base_user import BaseUserManager





class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(('Superuser must have is_active=True.'))        
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    username =  models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=40, unique=False, verbose_name='username', null=True)
    email = models.EmailField(max_length=100, blank=True, verbose_name='email', unique=True)
    mobile = models.CharField(max_length=20, blank=True, null=True, unique=True)
    otp = models.CharField(max_length=6, null=True)

    #profile_pic = models.ImageField(default="default-avatar.jpg", upload_to="image", null=True, blank=True)
    profile_pic = CloudinaryField('profile_pic')

    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    objects = CustomUserManager() 
    
    USERNAME_FIELD = 'email'        #REPLACE~LOGIN~AUTH~WITH~EMAIL
    REQUIRED_FIELDS = []            #REQUIRED~FIELDS~NONE



class Doctors(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    info = models.TextField(max_length=100)
    gender = models.CharField(max_length=10, null=True)
    
    dateofbirth = models.CharField(max_length=10, null=True)

    specialize = models.CharField(max_length=20, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors") 

    def __str__(self):
        return self.user.username



class Patients(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, null=True)

    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=20, null=True)
    district = models.CharField(max_length=20, null=True)

    dateofbirth = models.CharField(max_length=10, null=True)

    age = models.IntegerField()
    blood = models.CharField(max_length=50, null=True)
    heigh = models.CharField(max_length=10, null=True)
    weight = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients") 

    def __str__(self):
        return self.user.username



class Topics(models.Model):
    title = models.CharField(max_length=50, null=True)
    topic_image = CloudinaryField('topic_image')
    body = models.TextField(max_length=1500, null=True)

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics") 

    def __str__(self):
        return self.title



#CREATE~TOKEN~FOR~NEW~USERS
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
