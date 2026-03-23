from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Publisher, Author, Book, BookAuthor, BookInventory, BookMedia
from .serializers import (
    PublisherSerializer,
    AuthorSerializer,
    BookSerializer,
    BookAuthorSerializer,
    BookInventorySerializer,
    BookMediaSerializer,
)


class PublisherListCreateAPIView(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class PublisherRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'subtitle', 'description', 'isbn', 'language']
    ordering_fields = ['publish_date', 'title']

    def get_queryset(self):
        queryset = super().get_queryset()
        publisher = self.request.query_params.get('publisher')
        author = self.request.query_params.get('author')
        if publisher:
            queryset = queryset.filter(publisher_id=publisher)
        if author:
            queryset = queryset.filter(bookauthor__author_id=author)
        return queryset.distinct()


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookAuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookAuthor.objects.all()
    serializer_class = BookAuthorSerializer


class BookAuthorRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = BookAuthor.objects.all()
    serializer_class = BookAuthorSerializer


class BookInventoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookInventory.objects.all()
    serializer_class = BookInventorySerializer


class BookInventoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookInventory.objects.all()
    serializer_class = BookInventorySerializer


class BookMediaListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookMedia.objects.all()
    serializer_class = BookMediaSerializer


class BookMediaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookMedia.objects.all()
    serializer_class = BookMediaSerializer


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'service': 'book-service'})
