from django.db import models
from Users.models import Doctors, Patients, CustomUser

from django.utils.translation import ugettext_lazy as _







class Reservations(models.Model):
    user = models.ForeignKey(CustomUser, related_name='reservations', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, related_name='reservations', on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
    createdate = models.DateTimeField(auto_now_add=True ,blank=True, null=True)
    opptdate = models.DateField(blank=True, null=True)

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