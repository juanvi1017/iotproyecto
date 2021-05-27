
from django.contrib import admin
from django.urls import path
from domotica import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  views.home),
    path('cifrar/',  views.cifrar),
    path('decifrar/',  views.decifrar),
] 