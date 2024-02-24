from django.urls import path
from .views import ProfilePictureAPIView,PortfolioAPIView
from .views import RatingCreateView, RatingListView, SellerOverallRatingView,SellerViewSet,EducationViewSet,LanguageViewSet,SkillViewSet
from rest_framework.routers import DefaultRouter
from .views import SellerListCreateView, SellerRetrieveUpdateView
from .views import SellerListView
from .views import ImageListCreateView, ImageRetrieveUpdateDestroyView
from django.urls import path, include
router = DefaultRouter()
router.register(r'sellers/(?P<user_id>[^/.]+)', SellerViewSet, basename='seller')
router.register(r'educations/(?P<seller_id>[^/.]+)', EducationViewSet, basename='education')
router.register(r'languages/(?P<seller_id>[^/.]+)', LanguageViewSet, basename='language')
router.register(r'skills/(?P<seller_id>[^/.]+)', SkillViewSet, basename='skill')
urlpatterns = [
    path('', include(router.urls)),
    # path('create-seller/', SellerAPIView.as_view(), name='create-seller'),
    path('profile-picture/',ProfilePictureAPIView.as_view(),name='profile-picture'),
    path('portfolio/',PortfolioAPIView.as_view(),name='protfolio'),
    path('<int:seller_id>/rating/', RatingCreateView.as_view(), name='rating-create'),
    path('<int:seller_id>/ratings/', RatingListView.as_view(), name='seller-rating-list'),
    path('<int:seller_id>/overall-rating/', SellerOverallRatingView.as_view(), name='seller-overall-rating'),
    path('sellers/', SellerListCreateView.as_view(), name='seller-list-create'),
    path('seller/', SellerRetrieveUpdateView.as_view(), name='seller-retrieve-update'),
    path('sellersinfo/', SellerListView.as_view(), name='seller-list'),
    path('images/', ImageListCreateView.as_view(), name='image-list-create'),
    path('images/<int:pk>/', ImageRetrieveUpdateDestroyView.as_view(), name='image-retrieve-update-destroy'),
]


