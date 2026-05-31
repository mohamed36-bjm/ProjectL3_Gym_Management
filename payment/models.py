from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seance = models.ForeignKey('creationcompte.Seance', on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=20)
    card_number = models.CharField(max_length=19)
    date_booked = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Reserver {self.user.username} - {self.type}"
    
