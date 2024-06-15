from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Default Django admin
    path('', include('base.urls')),  # Include URLs from the 'base' app
    path('custom_admin/', include('base.custom_admin_urls')),  # Custom admin URLs
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Redirect to home page
]
