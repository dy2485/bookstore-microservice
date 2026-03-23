from django.urls import path, re_path
from . import views

urlpatterns = [
    # Generic proxy route for all services
    # Pattern: /api/{service}/{endpoint}
    re_path(r'^(?P<service>\w+)/(?P<path>.*)$', views.proxy_request, name='proxy_service'),
    
    # Backward compatibility - direct auth proxy
    re_path(r'^auth/(?P<path>.*)$', views.proxy_auth, name='proxy_auth'),
]