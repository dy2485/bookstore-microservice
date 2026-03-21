from django.urls import path
from . import views

urlpatterns = [
    path('auth/<path:path>', views.proxy_auth, name='proxy_auth'),
]