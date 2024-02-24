from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Seller
from .Serializer import SellerSerializer,ProfilePictureSerializer,PortfolioSerializer
from .renderers import CustomStatusRenderer
from rest_framework import generics
import json
class SellerListCreateView(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if 'images' in self.request.data:
            seller_instance = serializer.save(user=self.request.user)  # Save the Seller instance

            # Create Image instances associated with the Seller
            images_data = self.request.data.getlist('images')
            for image_data in images_data:
                image_serializer = ImageSerializer(data={'seller': seller_instance.id, 'image': image_data})
                if image_serializer.is_valid():
                    image_serializer.save()
                else:
                    # Handle validation errors if needed
                    pass
        education_data = {
            'seller': seller_instance,
            'education': self.request.data.get('education'),
            'from_year': self.request.data.get('from_year'),
            'to_year': self.request.data.get('to_year'),
        }

        # Create Education instance
        Education.objects.create(**education_data)
        # languages_data_str = self.request.data.get('languages')
        # print(languages_data_str)
        #     # Split the string and remove extra spaces
        # languages_data = [lang.strip() for lang in languages_data_str.split(',')]

        # # Create Language instances
        # languages_instances = [Language(seller=seller_instance, name=language) for language in languages_data]
        # Language.objects.bulk_create(languages_instances)
        skill_data_str = self.request.data.get('skills')
        # print(skill_data_str)
            # Split the string and remove extra spaces
        skill_data = [skill.strip() for skill in skill_data_str.split(',')]

        # Create Skill instances
        skill_instances = [Skill(seller=seller_instance, name=skill) for skill in skill_data]
        Skill.objects.bulk_create(skill_instances)
        profile_picture_data = self.request.data.get('profile_picture')
            # Create ProfilePicture instance
        ProfilePicture.objects.create(seller=seller_instance, profile_picture=profile_picture_data)



class SellerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Seller.objects.get(user=self.request.user)
    
# class SellerAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     renderer_classes = [CustomStatusRenderer]
#     def post(self, request, *args, **kwargs):
#         data = request.data.copy()
#         serializer = SellerSerializer(data=data)

#         if serializer.is_valid():
#             # Create a new Seller instance but don't save it yet
#             new_seller = serializer.save(user=request.user)

#             # Now, since user is a OneToOneField, save the Seller instance
#             # and associate it with the authenticated user
#             new_seller.user = request.user
#             new_seller.save()

#             return Response(status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from .models import ProfilePicture,Portfolio
class ProfilePictureAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]
    def post(self, request, *args, **kwargs):
            seller = Seller.objects.get(user=request.user)
            profile_picture = ProfilePicture.objects.filter(seller=seller).first()

            data = request.data.copy()
            data['user'] = request.user.id

            if profile_picture:
                serializer = ProfilePictureSerializer(profile_picture, data=data, context={'seller': seller}, partial=True)
            else:
                serializer = ProfilePictureSerializer(data=data, context={'seller': seller})

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        seller = Seller.objects.get(user=request.user)
        profile_picture = ProfilePicture.objects.filter(seller=seller).first()

        if profile_picture:
            serializer = ProfilePictureSerializer(profile_picture)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Profile picture not found.'}, status=status.HTTP_404_NOT_FOUND)
    
class PortfolioAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]
    def post(self, request, *args, **kwargs):
            seller = Seller.objects.get(user=request.user)
            portfolio = Portfolio.objects.filter(seller=seller).first()

            data = request.data.copy()
            data['user'] = request.user.id

            if portfolio:
                serializer = PortfolioSerializer(portfolio, data=data, context={'seller': seller}, partial=True)
            else:
                serializer = PortfolioSerializer(data=data, context={'seller': seller})

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        seller = Seller.objects.get(user=request.user)
        portfolios = Portfolio.objects.filter(seller=seller)
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

from .models import Seller, Rating
from .Serializer import RatingSerializer
from notifications.models import Notification 
class RatingCreateView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [CustomStatusRenderer]
    def post(self, request, seller_id):
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        value = request.data.get("value")
        review = request.data.get("review", "")

        # Check if a rating already exists for the user and seller
        existing_rating = Rating.objects.filter(seller=seller, user=user).first()

        if existing_rating:
            # If a rating already exists, update its values
            existing_rating.value = value
            existing_rating.review = review
            existing_rating.save()
            serializer = RatingSerializer(existing_rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If no rating exists, create a new one
            rating = Rating(seller=seller, user=user, value=value, review=review)
            rating.save()
            serializer = RatingSerializer(rating)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
from rest_framework import generics
class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class SellerOverallRatingView(APIView):
    def get(self, request, seller_id):
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

        overall_rating = seller.calculate_overall_rating()
        return Response({"overall_rating": overall_rating}, status=status.HTTP_200_OK)
    

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
class SellerDetailViewset(viewsets.ModelViewSet):
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['overall_rating'] = instance.calculate_overall_rating()
        return Response(data)
    
from rest_framework import viewsets
from .models import Seller, Education, Language, Skill
from .Serializer import SellerSerializer, EducationSerializer,LanguageSerializer,SkillSerializer,SellerSerializer
from rest_framework.decorators import action
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Seller.objects.filter(user_id=user_id)

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return Education.objects.filter(seller__id=seller_id)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return Language.objects.filter(seller__id=seller_id)

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        return Skill.objects.filter(seller__id=seller_id)


from rest_framework import generics
from .models import Seller
from .Serializer import SellerinfoSerializer
import random
from django.db.models import Subquery, F, OuterRef, Exists
from jobpost.models import JobPost
class SellerListView(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerinfoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        invite = self.request.query_params.get('invite')
        user_id = self.request.query_params.get('user_id', None)

        if invite is not None:
            invite_id = int(invite)
                # Search for the Job with the given ID
            job = JobPost.objects.get(id=invite_id)
            job_skills = job.skills.values_list('name', flat=True)
            # Handle the case when 'invite' param is present in the URL
            invited_sellers = Notification.objects.filter(
                sender=self.request.user,
                recipient=OuterRef('user'),
            ).values('recipient')
            filtered_sellers =  Seller.objects.filter(skills__name__in=job_skills)
            sellers_with_invite = filtered_sellers.annotate(
            is_invited=Exists(Subquery(invited_sellers))
            ).exclude(is_invited=True, user=F('user'))
            
            return sellers_with_invite
            # print(filtered_sellers)
            # return Seller.objects.annotate(
            #     is_invited=Exists(Subquery(invited_sellers))
            # ).exclude(is_invited=True, user=F('user'))

        elif user_id == '0':
            # Handle the case when 'user_id' param is present and its value is '0'
            all_sellers = Seller.objects.all()
            total_sellers = all_sellers.count()

            if total_sellers <= 20:
                return all_sellers
            return random.sample(list(all_sellers), min(20, total_sellers))

        elif user_id is not None:
            # Handle the case when 'user_id' param is present and its value is not '0'
            return Seller.objects.filter(user__id=user_id)

        else:
            # Handle the case when neither 'invite' nor 'user_id' params are present
            return Seller.objects.filter(user__id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

from .models import Image
from .Serializer import ImageSerializer

class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only images associated with the authenticated user
        return Image.objects.filter(seller__user=self.request.user)

    def perform_create(self, serializer):
        # Set the seller based on the authenticated user
        seller = self.request.user.seller
        serializer.save(seller=seller)

    def create(self, request, *args, **kwargs):
        # Handle multiple images in one payload
        data_list = [{'image': image} for image in request.FILES.getlist('images')]
        serializer = self.get_serializer(data=data_list, many=True)


        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            print(serializer.data)
            return Response(serializer.data, status=201, headers=headers)
        else:
            return Response(serializer.errors, status=400)

class ImageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer