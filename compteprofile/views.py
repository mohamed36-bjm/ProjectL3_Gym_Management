import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from creationcompte.models import Seance, Inscription, AthleteProfile, CoachProfile,Notification
from shop.models import Product
@login_required
def athlete_profile_view(request):
    user = request.user
    
    all_seances = Seance.objects.all().order_by('heure')
   
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    products = Product.objects.all()

    if user.is_coach:
        profile = CoachProfile.objects.filter(user=user).first()
        seances_to_show = all_seances.filter(coach_name=user)
        role_label = 'coach'
    else:
        profile = AthleteProfile.objects.filter(user=user).first()
        seances_to_show = all_seances
        role_label = 'athlete'

    sessions_list = []
    for s in seances_to_show:
        is_user_registered = s.participants.filter(id=user.id).exists()
        jour_format = str(s.jour).strip().capitalize() 
        s.places_disponibles = max(0, min(s.places_disponibles, s.places_totale))
        sessions_list.append({
            'id': s.id,
            'type': s.type,
            'jour': jour_format, 
            'time': s.heure.strftime('%H:%M'),
            'places': s.places_disponibles,   
            'total': s.places_totale,        
            'salle': s.salle,
            'coach': s.coach_name.username,
            'is_registered': is_user_registered,
        })

    days_list = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()


    context = {
        'user': user,
        'profile': profile,
        'is_coach': user.is_coach,
        'role': role_label,
        'sessions_list': sessions_list,
        'sessions_json': json.dumps(sessions_list),
        'notifications': notifications,
        'days_list': days_list,
        'products': products,
        'unread_count': unread_count, 
    }
    return render(request, 'profile/compteprofile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        if user.is_coach:
            profile = user.coachprofile
            profile.specialite = request.POST.get('specialite', profile.specialite)
        else:
            profile = user.athleteprofile
            
            
            weight = request.POST.get('weight')
            height = request.POST.get('height')
            age = request.POST.get('age')
           
            profile.weight = weight if weight and weight.strip() != '' else None
            profile.height = height if height and height.strip() != '' else None
            profile.age = age if age and age.strip() != '' else None
            
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
            
        profile.save() 
            
        messages.success(request, "Profil mis à jour avec succès !")
        return redirect('athlete_profile_view') 
    return redirect('athlete_profile_view')
@login_required
def delete_notification(request, notif_id):
    if request.method == 'POST':
        notif = get_object_or_404(Notification, id=notif_id, user=request.user)
        notif.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error' , 'message': 'Méthode non autorisée'}, status=405)

@login_required
def creer_seance(request):
    if request.method == 'POST':
       
        type_seance = request.POST.get('type_seance')
        jour = request.POST.get('jour_seance')
        heure = request.POST.get('heure_seance')
        places = request.POST.get('places_totale')
        salle = request.POST.get('salle_seance')

       
        if not all([type_seance, jour, heure, places, salle]):
            messages.error(request, "Veuillez remplir tous les champs !")
            return redirect('/profile/#section-booking')

        try:
           
            conflit = Seance.objects.filter(
                jour=jour,
                heure=heure,
                salle=salle
            ).first()

            if conflit:
                messages.error(request, 
                    f"Impossible ! La {salle} est déjà réservée le {jour} à {heure} "
                    f"pour une séance de {conflit.type} par le coach {conflit.coach_name.username}."
                )
                return redirect('/profile/#section-booking')
            
            
            Seance.objects.create(
                type=type_seance,
                jour=jour,
                heure=heure,
                places_totale=int(places),        
                places_disponibles=int(places),   
                salle=salle,
                coach_name=request.user
            )

            
            Notification.objects.create(
                user=request.user,
                message=f"Nouvelle séance de {type_seance} créée pour le {jour} à {heure}."
            )

            messages.success(request, "Séance publiée avec succès !")
            return redirect('/profile/#section-booking')

        except Exception as e:
            messages.error(request, f"Erreur lors de la création : {str(e)}")
            return redirect('/profile/#section-booking')

    return redirect('athlete_profile_view')

@login_required
def booking(request, seance_id):
    if request.method == 'POST':
        try:
            seance = get_object_or_404(Seance, id=seance_id)
            
            if request.user in seance.participants.all():
                
                seance.participants.remove(request.user)
                seance.places_disponibles += 1  
                seance.save()
                
                Notification.objects.create(
                    user=request.user, 
                    message=f"Annulation réussie pour {seance.type}."
                )
                return JsonResponse({'status': 'success'})
            else:
               
                if seance.places_disponibles > 0:
                    seance.participants.add(request.user)
                    seance.places_disponibles -= 1 
                    seance.save()
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Complet'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error'}, status=400)
from django.db import transaction 

@login_required
def supprimer_seance(request, seance_id):
    if request.method == 'POST':
       
        seance = get_object_or_404(Seance, id=seance_id, coach_name=request.user)
        try:
          
            type_name = str(seance.type)
            jour_name = str(seance.jour)
           
            ids_athletes = list(Inscription.objects.filter(seance=seance).values_list('athlete_id', flat=True))
            seance.delete()
           
            Notification.objects.create(
                user=request.user,
                message=f"Séance de {type_name} du {jour_name} supprimée avec succès."
            )

           
            for a_id in ids_athletes:
                Notification.objects.create(
                    user_id=a_id,
                    message=f"Attention: La séance de {type_name} du {jour_name} a été annulée par le coach."
                )

            return JsonResponse({'status': 'success'})

        except Exception as e:
            if seance.id:
                seance.delete()
            return JsonResponse({'status': 'success', 'debug_msg': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=400)