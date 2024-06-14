from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('collections/', views.collection_list, name='collection_list'),
]
