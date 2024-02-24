from rest_framework import routers
from .views import JobProposalViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyDataAPIView
router = routers.DefaultRouter()
router.register(r'job-proposals', JobProposalViewSet)



urlpatterns = [
    # ...
    path('', include(router.urls)),
    path('mydata/', MyDataAPIView.as_view(), name='mydata-list'),
    # ...
]
