from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class BookCategory(models.Model):
    book_id = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book_id', 'category')

class BookTag(models.Model):
    book_id = models.IntegerField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book_id', 'tag')

class CatalogSearchHistory(models.Model):
    customer_id = models.IntegerField(null=True, blank=True)
    query = models.CharField(max_length=512)
    filters = models.JSONField(default=dict, blank=True)
    result_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
