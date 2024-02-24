from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from account.renderers import CustomStatusRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import SetRoleSerializer
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'status_code': status.HTTP_200_OK
    }


from Seller.models import Seller
class UserRegistrationView(APIView):
    renderer_classes = [CustomStatusRenderer]
    def post(self,request,format=None):
        if 'ReEmailaddress' in request.data:
            request.data.pop('ReEmailaddress')
        firstname = request.data.pop('firstname')
        lastname = request.data.pop('lastname')
        password2 = request.data.pop('Repassword')
        # no=request.data.pop('name')
        name = f"{firstname} {lastname}"
        data=request.data
        data['name'] = name
        data['password2'] = password2
        serializer =UserRegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            response_data = {
                'token': token,
                'msg': 'Registration success',
                'status_code': status.HTTP_201_CREATED,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        response_data = {
            'errors': serializer.errors,
            'status_code': status.HTTP_400_BAD_REQUEST,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
from Seller.Serializer import SellerinfoSerializer
from Client.models import Client
from Client.Serializer import ClientinfoSerializer
from decouple import config
class UserLoginView(APIView):
    renderer_classes = [CustomStatusRenderer]
    def post(self,request,format=None):
        serializer= UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user = authenticate(email=email, password=password)
            seller_flag=False
            try:    
                seller = Seller.objects.get(user=user)
                    # Include seller information in the response

                seller_serializer = SellerinfoSerializer(seller)
                data = seller_serializer.data
                seller_flag=True
            except Seller.DoesNotExist:
                data = None
            try:    
                client = Client.objects.get(user=user)
                    # Include seller information in the response

                client_serializer = ClientinfoSerializer(client)
                data = client_serializer.data
            except Client.DoesNotExist:
                if seller_flag==False:
                    data = None
            if data is not None:
                try:
                    profile_picture_url = data['profile_picture']['profile_picture']
                    base_url = config('base_url')
                    full_url = f'{base_url}{profile_picture_url}'

                    # Update the response data with the new full URL
                    data['profile_picture']['profile_picture'] = full_url
                except:
                    pass
            if user is not None:
                token = get_tokens_for_user(user)
                response_data = {
                    'token': token,
                    'msg': 'Login success',
                    'status_code': status.HTTP_200_OK,
                    'user':data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'errors': {'non_field_errors': ['Email or password is not valid']},
                    'status_code': status.HTTP_404_NOT_FOUND,
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [CustomStatusRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    response_data = {
            'status_code': status.HTTP_200_OK,
            'data': serializer.data,
        }
    
    return Response(response_data)

class UserChangePasswordView(APIView):
  renderer_classes = [CustomStatusRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    response_data = {
            'msg': 'Password Changed Successfully',
            'status_code': status.HTTP_200_OK,
        }
    return Response(response_data)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [CustomStatusRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    response_data = {
            'msg': 'Password Reset link sent. Please check your Email',
            'status_code': status.HTTP_200_OK,
        }
    return Response(response_data)

class UserPasswordResetView(APIView):
  renderer_classes = [CustomStatusRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    response_data = {
            'msg':'Password Reset Successfully',
            'status_code': status.HTTP_200_OK,
        }
    return Response(response_data)

  
class EmailActivationAPIView(APIView):
    def get(self, request, email_token, format=None):
            try:
                user_profile = User.objects.get(email_token=email_token)
                user_profile.is_email_verified = True
                user_profile.save()

                serializer = UserProfileSerializer(user_profile)
                response_data = {
            'status_code': status.HTTP_200_OK,
            'data': serializer.data,
            }
                return Response(response_data)  


            except User.DoesNotExist:
                return Response({'error': 'Invalid email token.'}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetRoleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SetRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            role = serializer.validated_data.get('role')
            user.role = role
            user.save()
            response_data = {
                "message": "Role updated successfully.",
                "status_code": status.HTTP_200_OK,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        response_data = {
            "errors": serializer.errors,
            "status_code": status.HTTP_400_BAD_REQUEST,
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class GetRole(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        role = user.role
        response_data = {
            "role": role,
            "status_code": status.HTTP_200_OK,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from .serializers import UserSerializer
class UserView(ListAPIView):
	queryset = User.objects.all().order_by('name')
	serializer_class = UserSerializer
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		excludeUsersArr = []
		try:
			excludeUsers = self.request.query_params.get('exclude')
			if excludeUsers:
				userIds = excludeUsers.split(',')
				for userId in userIds:
					excludeUsersArr.append(int(userId))
		except:
			return []
		return super().get_queryset().exclude(id__in=excludeUsersArr)