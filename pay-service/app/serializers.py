from rest_framework import serializers
from .models import PaymentMethod, PaymentIntent, PaymentTransaction, Refund, PaymentWebhook

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = '__all__'

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = '__all__'

class PaymentWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentWebhook
        fields = '__all__'
