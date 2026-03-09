import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from creationcompte.models import Seance, Inscription, AthleteProfile, CoachProfile,Notification
@login_required
def athlete_profile_view(request):
    user = request.user
    
    all_seances = Seance.objects.all().order_by('heure')
    notifications = Notification.objects.filter(user=user).order_by('-created_at')[:10]

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
            'places': s.places_disponibles,   # نرسل الرقم المتاح مباشرة
            'total': s.places_totale,        # نرسل الإجمالي الثابت
            'salle': s.salle,
            'coach': s.coach_name.username,
            'is_registered': is_user_registered,
        })

    days_list = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

    context = {
        'user': user,
        'profile': profile,
        'is_coach': user.is_coach,
        'role': role_label,
        'sessions_list': sessions_list,
        'sessions_json': json.dumps(sessions_list),
        'notifications': notifications,
        'days_list': days_list,
    }
    return render(request, 'profile/compteprofile.html', context)

@login_required
def creer_seance(request):
    if request.method == 'POST':
        # 1. استلام البيانات من الفورم
        type_seance = request.POST.get('type_seance')
        jour = request.POST.get('jour_seance')
        heure = request.POST.get('heure_seance')
        places = request.POST.get('places_totale')
        salle = request.POST.get('salle_seance')

        # 2. التحقق من ملء جميع الحقول
        if not all([type_seance, jour, heure, places, salle]):
            messages.error(request, "Veuillez remplir tous les champs !")
            return redirect('/profile/#section-booking')

        try:
            # 3. التحقق من وجود تضارب (نفس اليوم والساعة والقاعة)
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
            
            # 4. إنشاء الحصة مع ضبط المقاعد المتاحة لتساوي الإجمالي في البداية
            Seance.objects.create(
                type=type_seance,
                jour=jour,
                heure=heure,
                places_totale=int(places),        # الرقم الذي حدده المدرب
                places_disponibles=int(places),   # نجعله مساوياً للإجمالي عند الإنشاء
                salle=salle,
                coach_name=request.user
            )

            # 5. إنشاء إشعار للمدرب
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
                # --- حالة الإلغاء ---
                seance.participants.remove(request.user)
                seance.places_disponibles += 1  # نزيد المتاح فقط
                seance.save()
                
                Notification.objects.create(
                    user=request.user, 
                    message=f"Annulation réussie pour {seance.type}."
                )
                return JsonResponse({'status': 'success'})
            else:
                # --- حالة الحجز المباشر ---
                if seance.places_disponibles > 0:
                    seance.participants.add(request.user)
                    seance.places_disponibles -= 1 # ننقص المتاح فقط
                    seance.save()
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Complet'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error'}, status=400)
from django.db import transaction # أضف هذا الاستيراد في الأعلى

@login_required
def supprimer_seance(request, seance_id):
    if request.method == 'POST':
        # 1. جلب الحصة والتأكد أن المدرب هو صاحبها
        seance = get_object_or_404(Seance, id=seance_id, coach_name=request.user)
        
        try:
            # 2. حفظ المعلومات الأساسية قبل الحذف
            type_name = str(seance.type)
            jour_name = str(seance.jour)
            
            # 3. جلب قائمة المتدربين (Athletes) المسجلين في هذه الحصة
            # استعملنا .athlete_id لأن الحقل في الموديل اسمه athlete
            ids_athletes = list(Inscription.objects.filter(seance=seance).values_list('athlete_id', flat=True))

            # 4. حذف الحصة نهائياً (هذا سيحذف الـ Inscriptions تلقائياً)
            seance.delete()

            # 5. إرسال إشعار للمدرب (صاحب الحصة)
            Notification.objects.create(
                user=request.user,
                message=f"Séance de {type_name} du {jour_name} supprimée avec succès."
            )

            # 6. إرسال الإشعارات للمتدربين الذين كانوا مسجلين
            for a_id in ids_athletes:
                Notification.objects.create(
                    user_id=a_id, # هنا نربط الإشعار بـ ID المستخدم (المتدرب)
                    message=f"Attention: La séance de {type_name} du {jour_name} a été annulée par le coach."
                )

            return JsonResponse({'status': 'success'})

        except Exception as e:
            # في حال حدوث أي خطأ، نضمن حذف الحصة على الأقل
            if seance.id:
                seance.delete()
            return JsonResponse({'status': 'success', 'debug_msg': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=400)