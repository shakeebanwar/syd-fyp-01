from rest_framework import serializers
from .models import Client, ProfilePicture
from django_countries.fields import CountryField
from django_countries.serializer_fields import CountryField

# Serializer for profile picture update
class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ['profile_picture']
        extra_kwargs = {
            'profile_picture': {'required': True}
        }

    def update(self, instance, validated_data):
        # Update the profile_picture field of the existing ProfilePicture instance
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance

    def create(self, validated_data):
        # Since you are using a one-to-one relationship, you can create the ProfilePicture here
        client = self.context.get('client')
        validated_data['client'] = client
        profile_picture = ProfilePicture.objects.create(**validated_data)
        return profile_picture

# serializers.py in Client app
from rest_framework import serializers
from .models import Client





    
# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Client, ProfilePicture

User = get_user_model()


from account.serializers import UserSerializer
class ClientupdateSerializer(serializers.ModelSerializer):
    profile_picture = ProfilePictureSerializer()
    country = serializers.CharField(source='get_country_display', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Client
        fields = ('user', 'description', 'country', 'city', 'profile_picture')
    def __init__(self, *args, **kwargs):
        super(ClientupdateSerializer, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

from account.serializers import UserSerializer
class ClientinfoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    profile_picture = ProfilePictureSerializer()
    country = serializers.CharField(source='get_country_display', read_only=True)

    class Meta:
        model = Client
        fields = ('user', 'description', 'country', 'city', 'profile_picture')

        
from rest_framework import serializers
from .models import Recent_Freelancer
from Seller.Serializer import SellerinfoSerializer,RatingSerializer
class RecentFreelancerSerializer(serializers.ModelSerializer):
    recent_freelancer = SellerinfoSerializer()
    class Meta:
        model = Recent_Freelancer
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='get_country_display',read_only=True)
    profile_picture = ProfilePictureSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ('user', 'description', 'country', 'city','profile_picture')



