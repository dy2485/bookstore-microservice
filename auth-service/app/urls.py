from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    # Password Management
    path('password/change/', views.change_password, name='change_password'),
    path('password/reset/request/', views.reset_password_request, name='reset_password_request'),
    path('password/reset/confirm/', views.reset_password_confirm, name='reset_password_confirm'),
    
    # Token Management
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', views.verify_token, name='verify_token'),
    
    # Role Management (Admin only)
    path('roles/', views.list_roles, name='list_roles'),
    path('roles/assign/', views.assign_role, name='assign_role'),
    path('roles/remove/<int:user_id>/<str:role_name>/', views.remove_role, name='remove_role'),
]