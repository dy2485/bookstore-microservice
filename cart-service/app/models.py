from django.db import models

class Cart(models.Model):
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()
    qty = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

class CartPromo(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    promo_code = models.CharField(max_length=64)
    discount_amt = models.DecimalField(max_digits=10, decimal_places=2)

class CartLock(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    locked_until = models.DateTimeField()
