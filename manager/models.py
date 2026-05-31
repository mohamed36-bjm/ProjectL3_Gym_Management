from django.db import models

# Create your models here.
from django.conf import settings

class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    image = models.ImageField(upload_to="notifications/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.message[:30]
    