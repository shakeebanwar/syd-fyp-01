from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from .renderers import CustomStatusRenderer
from .models import Course, Video, UserProgress
from .serializers import CourseSerializer, VideoSerializer, UserProgressSerializer,CourseCreateSerializer,VideoUploadSerializer
from notifications.util import send_course_notification
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]
    def list(self, request, *args, **kwargs):
        response_data = []

        for course in self.queryset:
            videos = course.videos.all()
            total_videos = videos.count()
            progress_percent = 0
            watched_videos = 0
            for video in videos:
                try:
                    user_progress = UserProgress.objects.get(user=request.user, video=video)
                    if user_progress.watched:
                        watched_videos += 1
                except UserProgress.DoesNotExist:
                    pass
            if watched_videos > 0:
                progress_percent = (watched_videos / total_videos) * 100
            course_completed = watched_videos == total_videos

            course_data = {
                'user_id': request.user.id,
                'id': course.id,
                'title':course.title,
                'watched_videos': watched_videos,
                'total_videos': total_videos,
                'course_completed': course_completed,
                'progress_percent':progress_percent,
                'description':course.description,
                'total_duration':course.total_duration,
                'thumbnail': course.thumbnail.url if course.thumbnail else None
            }

            response_data.append(course_data)

        return Response(response_data, status=status.HTTP_200_OK)

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]

    @action(detail=False, methods=['GET'])
    def videos_in_course(self, request, course_id=None):
        # Retrieve all videos in a specific course
        videos = Video.objects.filter(course=course_id)
        serializer = VideoSerializer(videos, many=True, context={'request': request})

        # serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['post'])
    def mark_as_watched(self, request, pk=None):
        video = self.get_object()
        user = request.user

        # Check if a UserProgress record already exists for this video and user
        user_progress, created = UserProgress.objects.get_or_create(user=user, video=video)

        if not user_progress.watched:
            user_progress.watched = True
            user_progress.save()
            course = video.course
            videos = course.videos.all()
            total_videos = videos.count()

            watched_videos = 0
            for video in videos:
                try:
                    user_progress = UserProgress.objects.get(user=user, video=video)
                    if user_progress.watched:
                        watched_videos += 1
                except UserProgress.DoesNotExist:
                    pass

            if watched_videos == total_videos:
                user=self.request.user
                account= user.account
                user.account.connects+=100
                account.save()  
                send_course_notification(request.user,100,course.title)
            return Response({'message': f'Video "{video.title}" marked as watched by {user.name}.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': f'Video "{video.title}" was already marked as watched by {user.name}.'}, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['GET'])
    def video_by_id(self, request, pk=None):
        video = self.get_object()

        # Get all video IDs in the same course
        video_ids_in_course = Video.objects.filter(course=video.course).values_list('id', flat=True)

        # Find the index of the current video's ID in the list
        current_video_index = list(video_ids_in_course).index(video.id)

        # Calculate the index of the next and previous videos
        next_video_index = current_video_index + 1 if current_video_index < len(video_ids_in_course) - 1 else None
        previous_video_index = current_video_index - 1 if current_video_index > 0 else None

        # Get the next and previous video IDs based on the calculated indices
        next_video_id = video_ids_in_course[next_video_index] if next_video_index is not None else None
        previous_video_id = video_ids_in_course[previous_video_index] if previous_video_index is not None else None

        # Serialize the current video and include the next and previous video IDs
        serializer = VideoSerializer(video)
        data = serializer.data
        data['next_video_id'] = next_video_id
        data['previous_video_id'] = previous_video_id

        return Response(data)

class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]

    @action(detail=False, methods=['GET'])
    def course_progress(self, request, course_id):
        user = request.user
        print(course_id)
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': f'Course with id {course_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        videos = course.videos.all()
        total_videos = videos.count()

        watched_videos = 0
        for video in videos:
            try:
                user_progress = UserProgress.objects.get(user=user, video=video)
                if user_progress.watched:
                    watched_videos += 1
            except UserProgress.DoesNotExist:
                pass

        course_completed = watched_videos == total_videos

        response_data = {
            'user_id': user.id,
            'course_id': course.id,
            'watched_videos': watched_videos,
            'total_videos': total_videos,
            'course_completed': course_completed,
            'description':course.description,
            'total_duration':course.total_duration

        }

        return Response(response_data)

class CourseCreateViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    renderer_classes = [CustomStatusRenderer]
    # permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        print("Received POST request to create a course.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        course_id = serializer.instance.id if serializer.instance else None


        response_data = {
            'course_id': course_id,
            'other_data': serializer.data,  # Include other serialized data if needed
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoUploadViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoUploadSerializer
    renderer_classes = [CustomStatusRenderer]

    @action(detail=False, methods=['POST'])
    def upload_video(self, request):
        title = request.data.get('title')
        course_id = request.data.get('course')
        uploaded_file = request.data.get('file')

        if not title or not course_id or not uploaded_file:
            return Response({'message': 'Title, course_id, and file are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': f'Course with id {course_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        video_data = {
            'title': title,
            'course': course,
            'file': uploaded_file,
        }

        serializer = VideoUploadSerializer(data=video_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


