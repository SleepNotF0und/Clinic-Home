from django.db import models
from Users.models import Doctors, Patients, CustomUser
from DoctorActions.models import Clinics 

from django.utils.translation import gettext_lazy as _







class Reservations(models.Model):
    user = models.ForeignKey(CustomUser, related_name='reservations', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, related_name='reservations', on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinics, related_name='reservations', on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
    createdate = models.DateTimeField(auto_now_add=True ,blank=True, null=True)
    opptdate = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    def __str__(self):
        return self.user.username



class Comments(models.Model):
    user = models.ForeignKey(CustomUser, related_name='comments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, related_name='comments', on_delete=models.CASCADE)

    comment = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments") 
    
    def __str__(self):
        return self.comment



class Thanks(models.Model):
    user = models.ForeignKey(CustomUser, related_name='Thanks', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, related_name='Thanks', on_delete=models.CASCADE)

    thanks = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = _("Thank")
        verbose_name_plural = _("Thanks") 



class Previews(models.Model):
    user = models.ForeignKey(CustomUser, related_name='Previews', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, related_name='Previews', on_delete=models.CASCADE)

    preview = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name = _("Preview")
        verbose_name_plural = _("Previews") 


    