from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_coach = models.BooleanField(default=False)
    is_athlete = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)

class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialite = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    certificat = models.FileField(upload_to='certificates/', blank=True, null=True)
class AthleteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cas_medicale = models.TextField(blank=True, null=True)
class Seance(models.Model):
    coach_name = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    jour = models.CharField(max_length=20)
    heure = models.TimeField()
    places_totale = models.IntegerField()
    places_disponibles = models.IntegerField()
    salle = models.CharField(max_length=50, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='seances_reservees', blank=True)
class Inscription(models.Model):
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    seance = models.ForeignKey(Seance, related_name='inscriptions', on_delete=models.CASCADE)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}..."