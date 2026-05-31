from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from creationcompte.models import User, Notification, Seance
from shop.models import Product, Order

@login_required
def manager_statistiques(request):
   
    total_athletes = User.objects.filter(is_athlete=True).count()
    total_coaches = User.objects.filter(is_coach=True).count()
    

    total_sales_query = Order.objects.aggregate(total_revenue=Sum('product__price'))
    total_sales = total_sales_query['total_revenue'] if total_sales_query['total_revenue'] else 0
    total_orders = Order.objects.count()

   
    sport_stats = Seance.objects.values('type').annotate(count=Count('id'))
    
  
    sport_labels = [stat['type'] for stat in sport_stats]
    sport_counts = [stat['count'] for stat in sport_stats]

    return render(request, "manager/statistiques.html", {
        "total_athletes": total_athletes,
        "total_coaches": total_coaches,
        "total_sales": total_sales,
        "total_orders": total_orders,
        "sport_labels": sport_labels,
        "sport_counts": sport_counts,
    })
@login_required
def manager_dashboard(request):
    role = request.GET.get("role")
    search_name = request.GET.get("search_name")
    sport_type = request.GET.get("sport")

    users = User.objects.all()

    if role == "coach":
        users = users.filter(is_coach=True)
    elif role == "athlete":
        users = users.filter(is_athlete=True)

    if search_name:
        users = users.filter(username__icontains=search_name)

   
    if sport_type:
        users = users.filter(
            Q(seance__type__icontains=sport_type) | 
            Q(seances_reservees__type__icontains=sport_type)
        ).distinct()

    return render(request, "manager/dashboard.html", {
        "users": users,
        "selected_role": role,
        "search_name": search_name,
        "selected_sport": sport_type
    })

@login_required
def user_info(request, user_id):
    
    u = get_object_or_404(User, id=user_id)
    
    if u.is_coach:
        seances = Seance.objects.filter(coach_name=u)
    else:
        seances = u.seances_reservees.all()

   
    user_purchases = Order.objects.filter(user=u).select_related('product')    

    if request.method == "POST":
        if "delete_user" in request.POST:
            u.delete()
            messages.success(request, f"L'utilisateur {u.username} a été supprimé.")
            return redirect('manager_dashboard')

        if "update_info" in request.POST:
            u.username = request.POST.get("username")
            u.email = request.POST.get("email")
            u.phone = request.POST.get("phone")
            u.save()

            if u.is_athlete:
                profile = u.athleteprofile
                profile.weight = request.POST.get("weight")
                profile.height = request.POST.get("height")
                profile.age = request.POST.get("age")
                profile.save()
            elif u.is_coach:
                profile = u.coachprofile
                profile.specialite = request.POST.get("specialite")
                profile.bio = request.POST.get("bio")
                profile.save()

            messages.success(request, "Informations mises à jour.")
            return redirect('user_info', user_id=u.id)
       
        if "update_seance" in request.POST:
            seance_id = request.POST.get("seance_id")
           
            seance_obj = get_object_or_404(Seance, id=seance_id)
            
           
            try:
                
                seance_obj.type = request.POST.get("type")
                seance_obj.jour = request.POST.get("jour")
                seance_obj.heure = request.POST.get("heure")
                seance_obj.salle = request.POST.get("salle")
                seance_obj.save()

                messages.success(request, "La séance a été modifiée مع نجاح.") 
            except Exception as e:
                messages.error(request, f"Erreur de format : {e}")       

            return redirect('user_info', user_id=u.id)
       
        if "mark_delivered" in request.POST:
            order_id = request.POST.get("order_id")
            order_obj = get_object_or_404(Order, id=order_id)
            order_obj.is_delivered = True  
            order_obj.save()
            messages.success(request, f"Livraison confirmée pour: {order_obj.product.name}")
            return redirect('user_info', user_id=u.id)

    return render(request, "manager/user_info.html", {"u": u, "seances": seances, "user_purchases": user_purchases})

@login_required
def send_notification(request):
    if request.method == "POST":
        message = request.POST.get("message")
        image = request.FILES.get("image")
        role = request.POST.get("role")

        if role == "coach":
            target_users = User.objects.filter(is_coach=True)
        elif role == "athlete":
            target_users = User.objects.filter(is_athlete=True)
        else:
            target_users = User.objects.all()

      
        first_user = target_users.first()
        if first_user:
            first_notif = Notification.objects.create(user=first_user, message=message, image=image)
            
          
            for user_obj in target_users[1:]:
                Notification.objects.create(
                    user=user_obj,
                    message=message,
                    image=first_notif.image 
                )

        messages.success(request, "Notification envoyée.")
        return redirect("manager_dashboard")
    return redirect("manager_dashboard")

@login_required
def manage_shop(request):
   
    products = Product.objects.all()
    
    if request.method == "POST":
       
        if "add_product" in request.POST:
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            image = request.FILES.get('image')
            
            Product.objects.create(
                name=name, 
                price=price, 
                stock=stock, 
                image=image
            )
            messages.success(request, "Produit ajouté avec succès !")
            return redirect('manage_shop')

     
        if "delete_product" in request.POST:
            product_id = request.POST.get('product_id')
            product_obj = get_object_or_404(Product, id=product_id)
            product_obj.delete()
            messages.success(request, "Produit supprimé !")
            return redirect('manage_shop')

    return render(request, "manager/manage_shop.html", {"products": products})