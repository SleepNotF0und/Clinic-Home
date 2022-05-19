from django.db import models
from Users.models import Doctors, Patients, CustomUser

from django.utils.translation import gettext_lazy as _





class Notifications(models.Model):
    currentuser = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
    
    doctor = models.ForeignKey(Doctors, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(Patients, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)

    message = models.TextField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.message