from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from creationcompte.models import User

def login_view(request):
    if request.method == "POST":
        
        btn_type = request.POST.get("btn_type")

         
        if btn_type == "manager":
         
            manager_user = User.objects.filter(is_superuser=True).first() or User.objects.filter(is_coach=False, is_athlete=False).first()
            
            if manager_user:
               
                login(request, manager_user)
                return redirect("manager_dashboard")  
            else:
                messages.error(request, "Aucun compte manager trouvé dans la base de données.")
                return render(request, "login/login.html")

         
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)

               
                if user.is_coach or user.is_athlete:
                    return redirect("athlete_profile_view")  
                else:
                    return redirect("manager_dashboard")  

       
        messages.error(request, "Email ou mot de passe incorrect")
    return render(request, "login/login.html")
def manager_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:

            auth_user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if auth_user and (
                auth_user.is_superuser or
                (not auth_user.is_coach and not auth_user.is_athlete)
            ):
                login(request, auth_user)
                return redirect("manager_dashboard")

        messages.error(request, "Email ou mot de passe incorrect")

    return render(request, "login/manager_login.html")

    return render(request, "login/login.html")