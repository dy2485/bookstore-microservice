from django.db import models

class Customer(models.Model):
    user_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=1024, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=16, blank=True)

class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    label = models.CharField(max_length=64)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    is_default = models.BooleanField(default=False)

class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    prefer_genres = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomerActivity(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type = models.CharField(max_length=64)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CustomerWishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book_id = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'book_id')
