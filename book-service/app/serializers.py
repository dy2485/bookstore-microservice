from rest_framework import serializers
from .models import Publisher, Author, Book, BookAuthor, BookInventory, BookMedia

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthor
        fields = '__all__'

class BookInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInventory
        fields = '__all__'

class BookMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMedia
        fields = '__all__'
