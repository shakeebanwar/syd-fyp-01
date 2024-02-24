from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import JobPost
from .serializers import JobPostSerializer
from jobpost.renderers import CustomStatusRenderer
from django.db.models import Q
from rest_framework.decorators import action
from Client.models import Recent_Freelancer
from Seller.models import Seller
from account.models import User
from django.utils import timezone
from django.http import Http404
from Payment.models import Payment
from message.models import ChatRoom
from notifications.util import send_hire_notification
class JobPostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer] 
    def get_queryset(self):
        queryset = JobPost.objects.all()

        # Check if user wants to retrieve only their jobs
        if self.request.query_params.get('user_jobs') == 'true':
            queryset = queryset.filter(client=self.request.user.client)
        
        term = self.request.query_params.get('term')
        if term:
            queryset = queryset.filter(term=term)
        
        order_by = self.request.query_params.get('order_by')
        if order_by == 'most_recent':
            queryset = queryset.order_by('-created_time')  # - for descending order
        elif order_by == 'least_recent':
            queryset = queryset.order_by('created_time')
        if not queryset.exists():
        # Return an empty queryset
            return JobPost.objects.none()
        queryset = queryset.order_by('-created_time')
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})
    @action(detail=False, methods=['GET'])
    def search(self, request):
        term = self.request.query_params.get('term')
        queryset = JobPost.objects.all()

        if term:
            queryset = queryset.filter(
                Q(job_title__icontains=term) |
                Q(description__icontains=term)
            )

        serializer = JobPostSerializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=self.request.user.client)
            
            response_data = {
                'message': 'Job post created successfully.',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            if 'freelancer' in request.data:
            # Assuming the value is an ID of the Seller, you can update the freelancer field
                instance.freelancer_id = request.data['freelancer']
                freelancer=instance.freelancer_id
            serializer.save()
            response_data = {
                'message': 'Job post updated successfully.',
                'data': serializer.data
            }
            
            current_user=request.user.id
            try:
                seller_instance = get_object_or_404(Seller, user=freelancer)
                recent_freelancer_instance = Recent_Freelancer.objects.create(
                recent_freelancer=seller_instance,
                clients=current_user
                    # Add other fields relevant to the Recent_Freelancer model
                )
                chat_room = ChatRoom.objects.create(type='DM', name='Direct Message')
                chat_room.member.add(current_user, seller_instance.user)
                send_hire_notification(seller_instance.user,instance)
            except Http404:
            # Handle the case where the Seller with the given ID doesn't exist
                response_data = {
                    'error': 'Seller not found.',
                }

            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        
        response_data = {
            'message': 'Job post deleted successfully.',
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


from .serializers import SavedJobSerializer,SavedJobSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SavedJob
class SaveJobView(APIView):
    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer] 
    def post(self, request, job_post_id):
        job_post_id = int(job_post_id)
        job_post = get_object_or_404(JobPost, pk=job_post_id)
        saved_job, created = SavedJob.objects.get_or_create(seller=request.user.seller, job_post=job_post)
        if created:
            return Response({'message': 'Job saved successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Job is already saved.'}, status=status.HTTP_200_OK)
    def delete(self, request, job_post_id):
        job_post_id = int(job_post_id)
        job_post = get_object_or_404(JobPost, pk=job_post_id)
        saved_job = SavedJob.objects.filter(seller=request.user.seller, job_post=job_post)
        if saved_job.exists():
            saved_job.delete()
            return Response({'message': 'Job removed from saved list.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Job not found in saved list.'}, status=status.HTTP_404_NOT_FOUND)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})

class SavedJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved_jobs = SavedJob.objects.filter(seller=request.user.seller)
        serializer = SavedJobSerializer(saved_jobs, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})
    
class FreelancerJobPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_user = request.user
        balance=current_user.account.balance
        print(balance)
        job_posts = JobPost.objects.filter(freelancer=current_user)
        print("Current User:", current_user.id)
        print("Job Posts:", job_posts)
        serializer = JobPostSerializer(job_posts, many=True)
        response_data = {
            'balance': balance,
            'job_posts': serializer.data
        }

        return Response({'data': response_data}, status=status.HTTP_200_OK)
    

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import JobPost
from .serializers import JobPostUpdateSerializer
from notifications.util import send_seller_job_completed
class JobPostUpdateView(generics.UpdateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostUpdateSerializer
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the status is already 'completed'
        # if instance.status == 'completed':
        #     return Response({'error': 'JobPost already completed'}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        # Set the status to 'completed'
        request.data['status'] = 'completed'
        send_seller_job_completed(instance.freelancer,instance.job_title)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
