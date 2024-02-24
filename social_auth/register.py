
from django.contrib.auth import authenticate
from account.models import User
import random
from rest_framework.exceptions import AuthenticationFailed
from account.serializers import UserSerializer
from Seller.models import Seller
from Client.models import Client
from Client.Serializer import ClientinfoSerializer
from Seller.Serializer import SellerinfoSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from decouple import config
def generate_username(name):

    username = "".join(name.split(' ')).lower()
    # if not User.objects.filter(username=username).exists():
    return username
    # else:
    #     random_username = username + str(random.randint(0, 1000))
    #     return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)
    seller_flag=False

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            # registered_user = authenticate(
            #     email=email, password='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')
            user=User.objects.get(email=email)
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
                    print(data['profile_picture']['profile_picture'])
                except Exception as e:
                    print(f"Exception: {e}")
            if user is not None:
                tokens=user.tokens()
                
                return {
                    'email': user.email,
                    'username': user.name,
                    'tokens': user.tokens(),
                    'user': data
                }
                    #             'email': user.email,
                    # 'username': user.name,
                    # 'tokens': tokens,
                    # # 'user':data
            else:
                response_data = {
                    'errors': {'non_field_errors': ['Email or password is not valid']},
                    'status_code': status.HTTP_404_NOT_FOUND,
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
                # return {
                #     'username': registered_user.name,
                #     'email': registered_user.email,
                #     'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'name': generate_username(name), 'email': email,
            'password': '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'}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
        new_user=user
        # new_user = authenticate(
        #     email=email, password='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')

        return {
            'email': new_user.email,
            'username': new_user.name,
            'tokens': new_user.tokens()
        }
