from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProfilePictureAPIView, ClientCreateView, ClientDetailView
from django.conf.urls import include
from .views import ClientListView, ClientDetailView,CurrentUserClientView
from .views import RecentFreelancerListAPIView

urlpatterns = [
    path('update-profile-picture/', ProfilePictureAPIView.as_view(), name='update-profile-picture'),
    path('create/', ClientCreateView.as_view(), name='client-create'),
    path('clientupdate/', ClientListView.as_view(), name='client-list'),
    path('clients/<str:user_id>/', ClientDetailView.as_view(), name='client-detail'),
    path('current/', CurrentUserClientView.as_view(), name='current-client-detail'),
    path('api/recent_freelancers/', RecentFreelancerListAPIView.as_view(), name='recent_freelancers'),
]


