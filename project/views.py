from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import work,Project, Tag, Skill
from rest_framework.permissions import IsAuthenticated
from Seller.models import Seller
from .Serializer import WorkCreateSerializer,ProjectSerializer

class WorkCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the authenticated user making the request
        user = request.user
        data= request.data
        seller = Seller.objects.get(user=request.user)
        serializer = WorkCreateSerializer(data=data,context={'seller': seller})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        seller = Seller.objects.get(user=request.user)
        data['Seller']=seller
        serializer = ProjectSerializer(data=data,context={'seller': seller})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


