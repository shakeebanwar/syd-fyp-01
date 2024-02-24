"""djangoauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="APIs",
        default_version='1.0.0',
        description='API documentation'
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include(('account.urls', 'api/user'),namespace="api/user")),
    path('api/client/',include('Client.urls')),
    path('social_auth/', include(('social_auth.urls', 'social_auth'),namespace="social_auth")),
    path('api/seller/', include('Seller.urls')),
    path('api/project/', include('project.urls')),
    path('api/', include('jobpost.urls')),
    path('api/', include('JobProposal.urls')),
    path('api/', include('Payment.urls')),
    path('api/', include('Course.urls')),
    path('api/', include('dispute.urls')),
    path('api/v1/' ,include('message.urls')),
    path('api/v2/',
         include([
             path('account/',include(('account.urls','post'), namespace='account')),
             path('swagger/schema/',schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
         ])),
    path('api/', include('notifications.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('user/',include(('account.urls'))),
#     path('client/',include('Client.urls')),
#     path('social_auth/', include(('social_auth.urls', 'social_auth'),namespace="social_auth")),
#     path('seller/', include('Seller.urls')),
#     path('project/', include('project.urls')),
#     path('jobpost/', include('jobpost.urls')),
#     path('JobProposal/', include('JobProposal.urls')),
#     path('Payment/', include('Payment.urls')),
#     path('Course/', include('Course.urls')),
#     path('api/v1/',
#          include([
#             #  path('account/',include(('account.urls','post'), namespace='account')),
#              path('swagger/schema/',schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
#          ]))
# ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)