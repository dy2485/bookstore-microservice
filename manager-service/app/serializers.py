from rest_framework import serializers
from .models import ProductApproval, InventoryAudit, Promotion, PromotionBook, ManagerLog

class ProductApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductApproval
        fields = '__all__'

class InventoryAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryAudit
        fields = '__all__'

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class PromotionBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionBook
        fields = '__all__'

class ManagerLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerLog
        fields = '__all__'
