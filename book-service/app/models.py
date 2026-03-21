from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=512)
    subtitle = models.CharField(max_length=512, blank=True)
    description = models.TextField(blank=True)
    isbn = models.CharField(max_length=32, blank=True)
    language = models.CharField(max_length=64, blank=True)
    publish_date = models.DateField(null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'author')

class BookInventory(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    stock_qty = models.IntegerField(default=0)
    reserved_qty = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=0)

class BookMedia(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    file_url = models.URLField()
    type = models.CharField(max_length=64)
    caption = models.CharField(max_length=255, blank=True)
