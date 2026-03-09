

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from .models import AthleteProfile, CoachProfile

User = get_user_model()

def creationcompte(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('password')
        phone = request.POST.get('phone')
        role = request.POST.get('user_type')

        if User.objects.filter(username=u_name).exists():  
            messages.error(request, "Nom d'utilisateur déjà utilisé!")  
            return render(request, 'creationcompte/creationcompte.html')  

        user = User.objects.create_user(username=u_name, email=email, password=passw)
        user.phone = phone

        if role == 'coach':  
            user.is_coach = True
            user.is_athlete = False
            user.save()  
            CoachProfile.objects.create(
                user=user,
                specialite=request.POST.get('specialite'),
                bio=request.POST.get('bio'),
                certificat=request.FILES.get('certificat')
            )  
        else:  
            user.is_athlete = True
            user.is_coach = False
            user.save()
            AthleteProfile.objects.create(
                user=user,
                age=request.POST.get('age') or None,
                height=request.POST.get('height') or None,
                weight=request.POST.get('weight') or None,
                cas_medicale=request.POST.get('cas_medicale')
            )

        login(request, user)
        return redirect('athlete_profile_view')

    return render(request, 'creationcompte/creationcompte.html')
