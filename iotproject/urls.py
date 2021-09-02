
from django.contrib import admin
from django.urls import path
from domotica.views import (home, cifrar, decifrar)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  home),
    path('cifrar/',  cifrar, name = "cifrar"),
    path('decifrar/',  decifrar, name = "decifrar"),
] 