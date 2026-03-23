from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
import requests
import json

# Service URLs configuration
SERVICE_URLS = {
    'auth': 'http://auth-service:8000',
    'book': 'http://book-service:8000',
    'cart': 'http://cart-service:8000',
    'catalog': 'http://catalog-service:8000',
    'comments': 'http://comment-rate-service:8000',
    'customers': 'http://customer-service:8000',
    'orders': 'http://order-service:8000',
    'payments': 'http://pay-service:8000',
    'shipments': 'http://ship-service:8000',
    'staff': 'http://staff-service:8000',
    'managers': 'http://manager-service:8000',
}


@csrf_exempt
def proxy_request(request, service, path):
    """
    Generic proxy function to forward requests to microservices
    
    Usage: /api/{service}/{path}
    Example: /api/auth/login/ -> forwards to auth-service:8000/api/login/
    """
    service_lower = service.lower()
    
    if service_lower not in SERVICE_URLS:
        return HttpResponse(
            json.dumps({'error': f'Service "{service}" not found'}),
            status=404,
            content_type='application/json'
        )
    
    base_url = SERVICE_URLS[service_lower]
    target_url = f'{base_url}/api/{path}'
    
    # Prepare headers (remove host and content-length)
    headers = {}
    for key, value in request.headers.items():
        if key.lower() not in ['host', 'content-length']:
            headers[key] = value
    
    # Prepare request data
    try:
        if request.method in ['POST', 'PUT', 'PATCH']:
            data = request.body
        else:
            data = None
        
        # Forward request to target service
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=data,
            params=request.GET,
            timeout=10
        )
        
        # Return response
        return HttpResponse(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('content-type', 'application/json')
        )
    
    except requests.exceptions.Timeout:
        return HttpResponse(
            json.dumps({'error': 'Service request timeout'}),
            status=504,
            content_type='application/json'
        )
    except requests.exceptions.ConnectionError:
        return HttpResponse(
            json.dumps({'error': f'Cannot connect to {service} service'}),
            status=503,
            content_type='application/json'
        )
    except Exception as e:
        return HttpResponse(
            json.dumps({'error': f'Gateway error: {str(e)}'}),
            status=500,
            content_type='application/json'
        )


# Deprecated: separate proxy functions (kept for backward compatibility)
@csrf_exempt  
def proxy_auth(request, path):
    """Proxy to auth-service"""
    return proxy_request(request, 'auth', path)
    
    try:
        response = requests.request(method, auth_service_url, headers=headers, data=data, params=request.GET)
        return HttpResponse(response.content, status=response.status_code, content_type=response.headers.get('content-type'))
    except requests.RequestException as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
