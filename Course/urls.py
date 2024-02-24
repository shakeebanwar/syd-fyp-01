from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, VideoViewSet, UserProgressViewSet,CourseCreateViewSet,VideoUploadViewSet

# Create a router and register your viewsets with it.
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'user-progress', UserProgressViewSet)
router.register(r'course', CourseCreateViewSet)
router.register(r'video-uploads', VideoUploadViewSet, basename='video-upload')

urlpatterns = [
    path('', include(router.urls)),
    path('videos/<int:pk>/mark-as-watched/', VideoViewSet.as_view({'post': 'mark_as_watched'}), name='video-mark-as-watched'),
    path('courses/<int:course_id>/videos/', VideoViewSet.as_view({'get': 'videos_in_course'}), name='videos-in-course'),
    path('video-upload/', VideoUploadViewSet.as_view({'post': 'create'}), name='video-upload'),
    path('user-progress/progress/<int:course_id>/', UserProgressViewSet.as_view({'get': 'course_progress'}), name='course_progress'),
]
