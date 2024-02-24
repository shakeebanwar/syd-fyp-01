from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet
from .views import NotificationCreateView
router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send-notification/<int:user_id>/', NotificationCreateView.as_view(), name='send-notification'),
    # Add other URLs as needed

]


