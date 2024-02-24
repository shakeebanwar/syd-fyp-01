# in dispute/serializers.py
from rest_framework import serializers
from .models import Dispute
from account.serializers import UserSerializer
from jobpost.models import JobPost
class DisputeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    jobpost = serializers.PrimaryKeyRelatedField(queryset=JobPost.objects.all())
    class Meta:
        model = Dispute
        fields = '__all__'


class DisputeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = '__all__'

from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
