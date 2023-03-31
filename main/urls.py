from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('admin/', admin.site.urls),

path('', include('homepage.urls')),
path('1/', include('cinema_manager.urls')),
path('2/', include('cust.urls')),
path('3/', include('accountmanager.urls')),
path('4/', include('club_rep.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
