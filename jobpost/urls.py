from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobPostViewSet,SaveJobView,SavedJobsView,FreelancerJobPosts
from .views import JobPostUpdateView

router = DefaultRouter()
router.register(r'jobposts', JobPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('job-posts/search/', JobPostViewSet.as_view({'get': 'search'}), name='job-post-search'),
    path('save-job/<int:job_post_id>/', SaveJobView.as_view(), name='save-job'),
    path('saved-jobs/', SavedJobsView.as_view(), name='saved-jobs'),
    path('freelancer-jobposts/', FreelancerJobPosts.as_view(), name='freelancer-jobposts'),
    path('jobposts/<int:pk>/complete/', JobPostUpdateView.as_view(), name='complete_jobpost'),
]
