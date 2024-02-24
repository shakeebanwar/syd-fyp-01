from rest_framework import serializers
from .models import Course, Video, UserProgress

class CourseSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(use_url=True)
    class Meta:
        model = Course
        fields = '__all__'

class UserProgress2Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['watched']
class VideoSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    watched = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = '__all__'
    def get_watched(self, obj):
        # Get the current user
        user = self.context['request'].user

        # Check if the user has watched the video
        try:
            user_progress = UserProgress.objects.get(user=user, video=obj)
            return user_progress.watched
        except UserProgress.DoesNotExist:
            return False

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'
class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'file', 'course']
