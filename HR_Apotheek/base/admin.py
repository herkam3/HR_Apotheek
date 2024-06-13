from django.contrib import admin
from django.urls import path, include

urlpattern = [
    path('admin/', admin.site.urls),
    path("base/", include("base.urls")),
]