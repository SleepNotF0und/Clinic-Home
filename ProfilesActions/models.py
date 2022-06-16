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



class Chat(models.Model):

    doctor = models.ForeignKey(CustomUser, related_name='doctor_sender', on_delete=models.CASCADE, null=True, blank=True)
    patient = models.ForeignKey(CustomUser, related_name='patient_sender', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _("chat")
        verbose_name_plural = _("Chats")

    

class Messages(models.Model):

    chat_id = models.ForeignKey(Chat, related_name='chat', on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=1000, blank=True, null=True)
    sender = models.ForeignKey(CustomUser, related_name='sender', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.message
