from django.urls import path
from .views import ProjectCreateView,WorkCreateView

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('work/', WorkCreateView.as_view(), name='project-work'),

    
]