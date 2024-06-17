from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/<int:medicine_id>/', views.medicine_detail, name='medicine_detail'),
    path('collections/', views.collection_list, name='collection_list'),
    path('collections/<int:collection_id>/mark/', views.collection_mark_collected, name='collection_mark_collected'),
    path('custom_admin/collections/', views.admin_view_collections, name='admin_view_collections'),
    path('custom_admin/collections/<int:collection_id>/approve/', views.admin_approve_collection, name='admin_approve_collection'),
    path('custom_admin/collections/<int:collection_id>/delete/', views.admin_delete_prescription, name='admin_delete_prescription'),
    path('custom_admin/collections/create/', views.admin_create_prescription, name='admin_create_prescription'),
    path('custom_admin/medicines/', views.admin_manage_medicines, name='admin_manage_medicines'),
    path('custom_admin/medicines/add/', views.admin_add_medicine, name='admin_add_medicine'),
    path('custom_admin/medicines/<int:medicine_id>/edit/', views.admin_edit_medicine, name='admin_edit_medicine'),
    path('custom_admin/medicines/<int:medicine_id>/create_prescription/', views.admin_create_prescription_from_medicine, name='admin_create_prescription_from_medicine'),
    path('custom_admin/users/<int:user_id>/profile/', views.admin_view_user_profile, name='admin_view_user_profile'),  # Updated path
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('custom_admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
