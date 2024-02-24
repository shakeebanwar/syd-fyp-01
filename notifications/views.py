from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from notifications.renderers import CustomStatusRenderer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer] 


    @action(detail=False, methods=['GET'])
    def user_notifications(self, request):
        user = request.user
        notifications = Notification.objects.filter(recipient=user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['POST'])
    def mark_as_read(self, request):
        user = request.user
        notification_id = request.data.get('notification_id')

        try:
            notification = Notification.objects.get(id=notification_id, recipient=user)
            notification.mark_as_read()
            return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from django.contrib.auth import get_user_model
from jobpost.models import JobPost
User = get_user_model()

class NotificationCreateView(generics.CreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer] 

    def create(self, request, *args, **kwargs):
        sender = self.request.user
        recipient_id = self.kwargs.get('user_id')

        if not recipient_id:
            return Response({'error': 'recipient_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return Response({'error': 'Recipient not found'}, status=status.HTTP_404_NOT_FOUND)

        if recipient.role != 'seller':
            return Response({'error': 'Recipient is not a seller'}, status=status.HTTP_400_BAD_REQUEST)

        job_id = request.data.get('job_id', None)

        if not job_id:
            return Response({'error': 'job_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job_post = JobPost.objects.get(id=job_id)
            job_title = job_post.job_title
        except JobPost.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        content = f'You are invited by {sender.name} to a job called {job_title}'
        extras = {'job_id': job_id}
        notification_data = {
            'sender': sender.id,
            'recipient': recipient.id,
            'content': content,
            'extras': extras,
        }

        serializer = self.get_serializer(data=notification_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

        

