from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('reset-password/request/', views.reset_password_request, name='reset_password_request'),
    path('reset-password/confirm/', views.reset_password_confirm, name='reset_password_confirm'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
]