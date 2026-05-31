from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    
    path('login/', include('login.urls')),

    
    path('login/', include('login.urls')),
    path('profile/', include('compteprofile.urls')),
    path('creationcompte/', include('creationcompte.urls')),
    path('payment/', include('payment.urls')),
    path('manager/', include('manager.urls')),

    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('shop/', include('shop.urls')),
    path('', include('home.urls')),  
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)