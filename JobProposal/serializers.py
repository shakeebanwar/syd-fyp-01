from rest_framework import serializers
from .models import JobProposal
from Seller.models import Seller
from Seller.Serializer import SellerinfoSerializer
from jobpost.models import JobPost
from django.core.exceptions import ObjectDoesNotExist
class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ('job_title',)


class JobProposalSerializer(serializers.ModelSerializer):
    # seller = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    seller = SellerinfoSerializer(read_only=True)
    # job_post_title = JobPostSerializer(source='job_post.job_title', read_only=True)
    job_post_title = serializers.CharField(source='job_post.job_title', read_only=True)
    job_post_freelancer = serializers.CharField(source='job_post.freelancer', read_only=True)
    job_post_length = serializers.CharField(source='job_post.length', read_only=True)
    job_post_experience_needed = serializers.CharField(source='job_post.experience_needed', read_only=True)

    class Meta:
        model = JobProposal
        fields = '__all__'

    def create(self, validated_data):
        # Get the current user (assuming you are using authentication)
        # user = self.context['request'].user
        # client = Client.objects.get(user=user)

        # Assign the client field with the retrieved or created Client instance
        # validated_data['client'] = client
        # Create a new JobProposal instance with the client set to the current user
        job_proposal = JobProposal(**validated_data)
        job_proposal.save()

        job_post = job_proposal.job_post  
        job_post.numofproposals += 1

        try:
            job_post.save()
        except Exception as e:
            print(f"Error saving job post: {e}")
        return job_proposal
    def update(self, instance, validated_data):
        # Custom update method to handle partial updates
        instance.bid = validated_data.get('bid', instance.bid)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.cover_letter = validated_data.get('cover_letter', instance.cover_letter)
        instance.relevant_examples = validated_data.get('relevant_examples', instance.relevant_examples)
        instance.attachments = validated_data.get('attachments', instance.attachments)
        instance.job_post = validated_data.get('job_post', instance.job_post)
        instance.save()
        return instance