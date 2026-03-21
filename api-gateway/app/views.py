from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests

# Create your views here.

@csrf_exempt
def proxy_auth(request, path):
    # URL của auth-service (giả sử chạy trên port 8001)
    auth_service_url = f'http://auth-service:8001/api/{path}'
    
    # Forward the request
    method = request.method
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}
    data = request.body if request.method in ['POST', 'PUT', 'PATCH'] else None
    
    try:
        response = requests.request(method, auth_service_url, headers=headers, data=data, params=request.GET)
        return HttpResponse(response.content, status=response.status_code, content_type=response.headers.get('content-type'))
    except requests.RequestException as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
    # URL của auth-service (giả sử chạy trên port 8001)
    auth_service_url = f'http://auth-service:8001/api/{path}'
    
    # Forward the request
    method = request.method
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}
    data = request.body if request.method in ['POST', 'PUT', 'PATCH'] else None
    
    try:
        response = requests.request(method, auth_service_url, headers=headers, data=data, params=request.GET)
        return HttpResponse(response.content, status=response.status_code, content_type=response.headers.get('content-type'))
    except requests.RequestException as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
