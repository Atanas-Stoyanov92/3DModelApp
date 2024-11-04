from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Djangoadvanceproject.accounts.urls')),
    path('', include('Djangoadvanceproject.common.urls')),
    path('', include('Djangoadvanceproject.photos.urls')),
    path('', include('Djangoadvanceproject.threedmodel.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)