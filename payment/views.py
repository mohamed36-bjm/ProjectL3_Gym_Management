from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from django.contrib import messages
from .models import Reservation
from creationcompte.models import Seance, Notification 
from shop.models import Product, Order

def payer(request):
   
    seance_id = request.GET.get('seance_id')
    product_id = request.GET.get('product_id')

   
    if request.method == "GET":
        if product_id:
   
            item = get_object_or_404(Product, id=product_id)
            return render(request, 'payment/acheter.html', {'item': item})
        else:
            
            return render(request, 'payment/payment.html')

  
    if request.method == "POST":
        sub_numero = request.POST.get("sub-numero") 
        sub_cvv = request.POST.get("sub-cvv")      
        sub_date = request.POST.get("sub-date")    
        
        if not request.user.is_authenticated:
            messages.error(request, "Veuillez vous connecter d'abord")
            return redirect('login_view')

       
        if product_id:
            product_obj = get_object_or_404(Product, id=product_id)
            
            if product_obj.stock > 0:
                with transaction.atomic():
                    
                    Order.objects.create(
                        user=request.user,
                        product=product_obj
                    )
                    
                   
                    product_obj.stock -= 1
                    product_obj.save()

                  
                    Notification.objects.create(
                        user=request.user,
                        message=f"Achat réussi : {product_obj.name}. Vous pouvez le récupérer à la salle."
                    )
                
                messages.success(request, f"Paiement réussi pour {product_obj.name}")
                return redirect('athlete_profile_view')
            else:
                messages.error(request, "Désolé, ce produit n'est plus en stock.")
                return redirect('athlete_profile_view')

        
        elif seance_id:
            seance_obj = get_object_or_404(Seance, id=seance_id)
            sub_periode = request.POST.get("sub-periode") # (an, mois, séance)

            with transaction.atomic():
                
                Reservation.objects.create(
                    user=request.user,
                    seance=seance_obj,
                    type=sub_periode,
                    card_number=sub_numero
                )
                
               
                if request.user not in seance_obj.participants.all():
                    seance_obj.participants.add(request.user) 
                    seance_obj.places_disponibles -= 1
                    seance_obj.save()
                
               
                Notification.objects.create(
                    user=request.user,
                    message=f"Vous avez réservé la séance de {seance_obj.type} avec succes de paiement"
                )

            messages.success(request, "Succès du paiement et réservation effectuée")
            return redirect('athlete_profile_view')

    return redirect('athlete_profile_view')


def ReservationDetailes(request, seance_id):
    try:
        res = Reservation.objects.get(user=request.user, seance_id=seance_id)
        return JsonResponse({
            'status': 'success',
            'date_payement': res.date_booked.strftime('%d/%m/%Y'),
            'card_number': res.card_number 
        })
    except Reservation.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Réservation introuvable'}, status=404)


def CancelReservation(request, seance_id):
    if request.method == "POST":
        try:
            with transaction.atomic():
                reservation = Reservation.objects.get(user=request.user, seance_id=seance_id)
                seance = reservation.seance
                if seance:
                    seance.participants.remove(request.user)
                    seance.places_disponibles += 1
                    seance.save()
                reservation.delete()
                return JsonResponse({'status': 'success', 'message': 'Réservation annulée'})
        except Reservation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Réservation introuvable'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
        
# Create your views here.
def payer_achat(request, product_id):
    from shop.models import Product
    item = get_object_or_404(Product, id=product_id)
    
    
    return render(request, 'acheter/acheter.html', {'item': item})