
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    path('', include('main.urls')),
    #path("microsoft/", include("microsoft_auth.urls", namespace="microsoft_auth")),
]
