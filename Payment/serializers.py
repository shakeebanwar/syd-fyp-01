from rest_framework import serializers
from .models import Payment
from .models import Account,StripeAccount

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['job']
    extra_kwargs = {
            'job': {'required': True},  # Make the 'job' field required
        }
class PaymentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
    extra_kwargs = {
            'job': {'required': True},  # Make the 'job' field required
        }
class StripeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeAccount
        fields = ['account_id', 'created_at', 'completed']
