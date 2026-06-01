from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'BD Kutná Hora – Administrace'
admin.site.site_title = 'BD Kutná Hora'
admin.site.index_title = 'Správa obsahu'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nastenka.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
