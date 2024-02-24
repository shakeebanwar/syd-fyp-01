# in dispute/urls.py
from django.urls import path
from .views import DisputeListCreateView, DisputeUpdateResolvedView
from .views import ContactDetailView,ContactListCreateView


urlpatterns = [
    path('disputes/', DisputeListCreateView.as_view(), name='dispute-list-create'),
    path('disputes/resolve/<int:pk>/', DisputeUpdateResolvedView.as_view(), name='dispute-update-resolved'),
    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),

]
