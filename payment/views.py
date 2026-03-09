from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from creationcompte.models import Seance, Notification 
from django.contrib import messages
def payer(request):
    if request.method == "POST":
        sub_periode = request.POST.get("sub-periode")
        sub_numero = request.POST.get("sub-numero")
        seance_id = request.GET.get('seance_id')
        if request.user.is_authenticated:
            Reservation.objects.create(
                user=request.user,
                type=sub_periode,
                card_number=sub_numero
            )
            if seance_id:
                seance = get_object_or_404(Seance, id=seance_id)
                if request.user not in seance.participants.all():
                    seance.participants.add(request.user) 
                    seance.places_disponibles -= 1
                    seance.save()
                Notification.objects.create(
                    user=request.user,
                    message=f"Vous avez réservé avec succès la séance de {seance.type}."
                )

            messages.success(request, "Succès du paiement et réservation effectuée")
            return redirect('athlete_profile_view')
        else:
            messages.error(request, "Veuillez vous connecter d'abord")
            return redirect('login_view')
            
    return render(request, 'payment/payment.html')
# Create your views here.
