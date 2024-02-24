from django.urls import path
from account.views import EmailActivationAPIView,SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView
from .views import SetRoleAPIView, GetRole

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('activate/<email_token>', EmailActivationAPIView.as_view(), name="activate_email"),
    path('set-role/', SetRoleAPIView.as_view(), name='set-role'),
    path('get-role/', GetRole.as_view(), name='GetRole'),
]
