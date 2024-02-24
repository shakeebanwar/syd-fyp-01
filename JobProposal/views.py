# from rest_framework import viewsets
# from .models import JobProposal
# from .serializers import JobProposalSerializer  # You'll need to create this serializer

# class JobProposalViewSet(viewsets.ModelViewSet):
#     queryset = JobProposal.objects.all()
#     serializer_class = JobProposalSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import JobProposal
from .serializers import JobProposalSerializer
from rest_framework import renderers
from rest_framework.response import Response
import json

class CustomStatusRenderer(renderers.JSONRenderer):
    charset='utf-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response =''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else:
            response = json.dumps(data)
        return response

from rest_framework import status, serializers
class JobProposalViewSet(viewsets.ModelViewSet):
    queryset = JobProposal.objects.all()
    serializer_class = JobProposalSerializer
    renderer_classes = [CustomStatusRenderer] 
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed

    def get_queryset(self):
        queryset = JobProposal.objects.all()
        if self.request.query_params.get('job_post_id'):
            job_post_id = self.request.query_params.get('job_post_id')
            queryset = queryset.filter(job_post_id=job_post_id)
        else:
            # If job_post_id is not provided, filter by the current user
            try:
                queryset = queryset.filter(seller=self.request.user.seller)
                result_count = queryset.count()
                # You can optionally return the count in the API response
                self.queryset_count = result_count
            except:
                pass

        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})
    def perform_create(self, serializer):
        # Customize how a new JobProposal is created here, if needed
        user=self.request.user
        account= user.account
        if account.connects < 8:
            # If the user has insufficient connects, raise a validation error
            raise serializers.ValidationError({'details': ['Insufficient connects in account']})

        account.connects-=8
        account.save()
        serializer.save(seller=self.request.user.seller)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})
    def perform_update(self, serializer):
        # Customize how a JobProposal is updated here, if needed
        serializer.save()

    def perform_destroy(self, instance):
        # Customize how a JobProposal is deleted here, if needed
        instance.delete()


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from jobpost.models import JobPost
from decouple import config
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=config('OPENAI_API_KEY'),
)
def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
def generate_cover_letter_prompt(job):
    prompt = f"Write a cover letter for the position of {job.job_title}.\n\n"
    prompt += f"Job Title: {job.job_title}\n"
    prompt += f"Description: {job.description}\n"
    prompt += f"Experience Needed: {job.experience_needed}\n"
    prompt += f"Length: {job.length}\n"
    prompt += f"Skills Required: {job.skills}\n"
    prompt += f"Scope: {job.scope}\n"
    prompt += "\nNote: You are writing this cover letter as an individual so use dear Client, not for any specific company or manager.\n"
    prompt += "\ninstructions: Generate a letter with the following body:\n[Body of the letter goes here]\nAvoid including header information like [Your Name], [Your Address], [Today's Date], [Recipient's Name], etc..\n"

    return prompt
class MyDataAPIView(APIView):
    # renderer_classes = [CustomStatusRenderer] 

    def get(self, request, *args, **kwargs):
        # Create sample data (replace this with your own logic)
        job_id = request.query_params.get('job_id', None)

        if not job_id:
            return Response({"errors": {"details": ["Job ID is required"]}}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the job object based on the job ID
        try:
            job = JobPost.objects.get(id=job_id)
        except JobPost.DoesNotExist:
            return Response({"errors": {"details": ["Job not found"]}}, status.HTTP_404_NOT_FOUND)

        prompt= generate_cover_letter_prompt(job)
        # Call the chat_gpt function
        gpt_response = chat_gpt(prompt)
        print(gpt_response)
        # Return the GPT response in the API response
        return Response({"data": gpt_response}, status=status.HTTP_200_OK)
