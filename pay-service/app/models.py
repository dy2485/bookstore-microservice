from django.db import models

class PaymentMethod(models.Model):
    customer_id = models.IntegerField()
    provider = models.CharField(max_length=64)
    details = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

class PaymentIntent(models.Model):
    order_id = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=32, default='USD')
    status = models.CharField(max_length=64)
    client_secret = models.CharField(max_length=512)
    expires_at = models.DateTimeField()

class PaymentTransaction(models.Model):
    order_id = models.IntegerField()
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=64)
    provider_ref = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Refund(models.Model):
    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=64)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

class PaymentWebhook(models.Model):
    event_id = models.CharField(max_length=255, unique=True)
    provider = models.CharField(max_length=64)
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)
    handled_at = models.DateTimeField(null=True, blank=True)
