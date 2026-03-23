from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='book_health'),

    path('publishers/', views.PublisherListCreateAPIView.as_view(), name='publisher-list-create'),
    path('publishers/<int:pk>/', views.PublisherRetrieveUpdateDestroyAPIView.as_view(), name='publisher-detail'),

    path('authors/', views.AuthorListCreateAPIView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorRetrieveUpdateDestroyAPIView.as_view(), name='author-detail'),

    path('books/', views.BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),

    path('book-authors/', views.BookAuthorListCreateAPIView.as_view(), name='bookauthor-list-create'),
    path('book-authors/<int:pk>/', views.BookAuthorRetrieveDestroyAPIView.as_view(), name='bookauthor-detail'),

    path('inventories/', views.BookInventoryListCreateAPIView.as_view(), name='inventory-list-create'),
    path('inventories/<int:pk>/', views.BookInventoryRetrieveUpdateDestroyAPIView.as_view(), name='inventory-detail'),

    path('media/', views.BookMediaListCreateAPIView.as_view(), name='bookmedia-list-create'),
    path('media/<int:pk>/', views.BookMediaRetrieveUpdateDestroyAPIView.as_view(), name='bookmedia-detail'),
]