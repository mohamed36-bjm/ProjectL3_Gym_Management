from django.shortcuts import render

# Create your views here.


def home_view(request):
    return render(request, 'accounts/home.html')  # تأكد من أن القالب موجود