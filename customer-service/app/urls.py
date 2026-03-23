from django.urls import path
from . import views

urlpatterns = [
    # Profile Management
    path('profile/create/', views.create_or_get_profile, name='create_or_get_profile'),
    path('profile/', views.get_profile, name='get_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    # Extended Profile
    path('profile/extended/', views.manage_customer_profile, name='manage_customer_profile'),
    
    # Address Management
    path('addresses/', views.list_addresses, name='list_addresses'),
    path('addresses/create/', views.create_address, name='create_address'),
    path('addresses/<int:address_id>/', views.get_address, name='get_address'),
    path('addresses/<int:address_id>/update/', views.update_address, name='update_address'),
    path('addresses/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    
    # Wishlist Management
    path('wishlist/', views.list_wishlist, name='list_wishlist'),
    path('wishlist/<int:book_id>/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/<int:book_id>/remove/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/<int:book_id>/check/', views.check_wishlist, name='check_wishlist'),
    
    # Activity Log
    path('activity/', views.list_activity, name='list_activity'),
    path('activity/log/', views.log_activity, name='log_activity'),
]
