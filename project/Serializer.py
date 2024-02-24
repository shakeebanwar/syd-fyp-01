from rest_framework import serializers
from .models import work,Project, Tag, Skill
from Seller.models import Seller


class WorkCreateSerializer(serializers.Serializer):
    picture = serializers.ImageField()
    text = serializers.CharField()
    video = serializers.FileField(required=False)
    url = serializers.URLField(required=False)

    def create(self, validated_data):
        # Retrieve the seller instance from the context
        seller = self.context.get('seller')

        # Create the work instance using the validated data
        validated_data['Seller'] = seller
        work_instance = work.objects.create(**validated_data)

        return work_instance
    

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']
    def create(self, validated_data):
        Project = self.context.get('Project')
        skill = Skill.objects.create(Project=Project, **validated_data)
        return skill

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']
    def create(self, validated_data):
        Project = self.context.get('Project')
        tag = Tag.objects.create(Project=Project, **validated_data)
        return tag

class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Project
        fields = ('thumbnail', 'title', 'tags')

    def create(self, validated_data):
        # skill_data = validated_data.pop('skills')
        tags_data = validated_data.pop('tags')
        seller = self.context.get('seller')
        validated_data['Seller'] = seller
        project = Project.objects.create(**validated_data)
        # for tag_data in tags_data:
        #     tags=Tag.objects.create(Project=project, **tag_data)
        # for skill_item in skill_data:
        #     skill = Skill.objects.create(Project=project, **skill_item)

        return project

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name', 'Project')

