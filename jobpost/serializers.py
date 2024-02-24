from rest_framework import serializers
from .models import Skill, JobPost,SavedJob
from Seller.models import Seller
from rest_framework.response import Response
from rest_framework import status


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
class SavedJobinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = '__all__'
from Payment.serializers import PaymentGetSerializer,PaymentSerializer
class JobPostSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    client = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    payment = PaymentGetSerializer(read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = JobPost
        fields = '__all__'

    def get_saved_job(self, obj):
        user = self.context['request'].user
        saved_job = SavedJob.objects.filter(seller=user.seller, job_post=obj).first()
        if saved_job:
            return SavedJobSerializer(saved_job).data
        return None
    def create(self, validated_data):
        skills_data = validated_data.pop('skills')

        job_post = JobPost.objects.create(**validated_data)
        
        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(name=skill_data['name'])
            job_post.skills.add(skill)
        
        return job_post

    def update(self, instance, validated_data):
        # Update the main fields of the instance
        instance.term = validated_data.get('term', instance.term)
        instance.job_title = validated_data.get('job_title', instance.job_title)
        instance.scope = validated_data.get('scope', instance.scope)
        instance.length = validated_data.get('length', instance.length)
        instance.experience_needed = validated_data.get('experience_needed', instance.experience_needed)
        instance.hire_opp = validated_data.get('hire_opp', instance.hire_opp)
        instance.project_budget = validated_data.get('project_budget', instance.project_budget)
        instance.description = validated_data.get('description', instance.description)
        
        # Update the nested skills
        skills_data = validated_data.get('skills')
        if skills_data:
            for skill_data in skills_data:
                skill, created = Skill.objects.get_or_create(name=skill_data['name'])
                instance.skills.add(skill)

        instance.save()
        return instance
    def get_user(self, obj):
        user_data = {
            'id': obj.client.user.id,
        }
        return user_data

class SavedJobSerializer(serializers.ModelSerializer):
    job_post=JobPostSerializer()
    class Meta:
        model = SavedJob
        fields = '__all__'


from rest_framework import serializers
from .models import JobPost

class JobPostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ['status']
