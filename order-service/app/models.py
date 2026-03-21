from django.db import models

class Order(models.Model):
    customer_id = models.IntegerField()
    status = models.CharField(max_length=64)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=32)
    shipping_status = models.CharField(max_length=32)
    order_date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class OrderAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=32)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=32)

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    from_status = models.CharField(max_length=64)
    to_status = models.CharField(max_length=64)
    changed_by = models.IntegerField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

class OrderCoupon(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=64)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pay_id = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=32)
    provider = models.CharField(max_length=128)
    transaction_time = models.DateTimeField(auto_now_add=True)
