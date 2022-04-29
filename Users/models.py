from django.db import models
from django.db.models.signals import post_save

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from cloudinary.models import CloudinaryField 




class CustomUser(AbstractUser):
    username =  models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=40, unique=True, verbose_name='username')
    email = models.EmailField(max_length=100, blank=True, verbose_name='email', unique=False)
    mobile = models.CharField(max_length=20, blank=True, null=True, unique=False)
    otp = models.CharField(max_length=6)

    #profile_pic = models.ImageField(default="default-avatar.jpg", upload_to="image", null=True, blank=True)
    profile_pic = CloudinaryField('profile_pic')

    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)



class Doctors(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    info = models.TextField(max_length=100)
    gender = models.CharField(max_length=10, null=True)
    
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=20, null=True)
    district = models.CharField(max_length=20, null=True)
    
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



#CREATE TOKEN FOR NEW USERS
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
