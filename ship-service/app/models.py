from django.db import models

class Shipment(models.Model):
    order_id = models.IntegerField()
    carrier = models.CharField(max_length=128)
    tracking_number = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=64)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='items')
    order_item_id = models.IntegerField()
    qty = models.IntegerField()

class ShippingRate(models.Model):
    carrier = models.CharField(max_length=128)
    route_from = models.CharField(max_length=255)
    route_to = models.CharField(max_length=255)
    weight_from = models.DecimalField(max_digits=10, decimal_places=2)
    weight_to = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)

class ShippingAddress(models.Model):
    customer_id = models.IntegerField(null=True, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=32)

class ShipmentHistory(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)
    location = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
