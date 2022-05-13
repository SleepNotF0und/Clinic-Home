from django.db import models
from Users.models import CustomUser

from django.utils.translation import ugettext_lazy as _

from cloudinary.models import CloudinaryField 




class Clinics(models.Model):
    user = models.ForeignKey(CustomUser, related_name='clinics', on_delete=models.CASCADE)

    clinic_image = CloudinaryField('clinic_image', blank=True, null=True,)
    clinicname = models.CharField(max_length=70, blank=True, null=True, unique=True)
    workhours = models.CharField(max_length=40, blank=True, null=True)

    city = models.CharField(max_length=30, blank=True, null=True)
    district = models.CharField(max_length=40, blank=True, null=True)
    address = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        verbose_name = _("Clinic")
        verbose_name_plural = _("Clinics")

    def __str__(self):
        return self.clinicname

