from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product  
from payment.models import Reservation  

@login_required
def acheter(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        if product.stock <= 0:
            messages.error(request, f"Désolé, le produit {product.name} est épuisé.")
            return redirect('profile') 
        else:
            product.stock -= 1
            product.save()
            messages.success(request, f"Félicitations ! Vous avez acheté {product.name} pour {product.price} DZD.")
            return redirect('/profile/#section-shop')
    
    return redirect('profile')
