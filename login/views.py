

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('athlete_profile_view')
        else:
            return render(request, 'login/login.html', {'error': 'Nom ou mot de passe incorrect'})
    return render(request, 'login/login.html')