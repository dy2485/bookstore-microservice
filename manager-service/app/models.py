from django.db import models

class ProductApproval(models.Model):
    book_id = models.IntegerField()
    status = models.CharField(max_length=64)
    reviewer_id = models.IntegerField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class InventoryAudit(models.Model):
    book_id = models.IntegerField()
    qty_before = models.IntegerField()
    qty_after = models.IntegerField()
    reason = models.CharField(max_length=256)
    performed_by = models.IntegerField()
    performed_at = models.DateTimeField(auto_now_add=True)

class Promotion(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    type = models.CharField(max_length=64)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

class PromotionBook(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    book_id = models.IntegerField()

class ManagerLog(models.Model):
    user_id = models.IntegerField()
    action = models.CharField(max_length=128)
    target_type = models.CharField(max_length=64)
    target_id = models.IntegerField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
    at_time = models.DateTimeField(auto_now_add=True)
