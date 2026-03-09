from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # ✅ أضف هذا

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('creationcompte.urls')),
    path('login/', include('login.urls')),
    path('profile/', include('compteprofile.urls')),
    path('creationcompte/', include('creationcompte.urls')),
    path('payment/', include('payment.urls')),
]

# هذا الجزء يسمح لملفات MEDIA (مثل شهادات المدربين) بالظهور أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)