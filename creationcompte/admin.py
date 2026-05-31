from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, CoachProfile, AthleteProfile, Seance, Inscription, Notification

admin.site.register(User)
admin.site.register(CoachProfile)
admin.site.register(AthleteProfile)
admin.site.register(Seance)
admin.site.register(Inscription)
admin.site.register(Notification)