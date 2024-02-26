from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import PaymentSerializer
import stripe
import os

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer  # Import the Account serializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    # Additional custom actions can be added here

    @action(detail=False, methods=['GET'])
    def user_accounts(self, request, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid user ID format"}, status=status.HTTP_400_BAD_REQUEST)

        accounts = Account.objects.filter(user=user_id)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def current_user(self, request):
        user = request.user  # Get the current authenticated user
        accounts = Account.objects.filter(user=user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    



# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from .models import StripeAccount

# class CreateStripeAccount(APIView):
#     def post(self, request):
#         try:
#             # Create a Stripe account
#             account = stripe.Account.create(
#                 type="express",  # You can change the account type as needed
#             )

#             return Response({'message': 'Stripe account created successfully', 'account_id': account.id})
#         except Exception as e:
#             return Response({'error': str(e)})
class CreateStripeAccount(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            existing_stripe_account = StripeAccount.objects.filter(user=request.user).first()
            if existing_stripe_account:
                # If an account already exists, return its details
                return Response({
                    'account_id': existing_stripe_account.account_id,
                }, status=status.HTTP_200_OK)
            # Create a Stripe account
            account = stripe.Account.create(
                type="express",  # You can change the account type as needed
            )

            # Get the authenticated user
            user = request.user

            # Create and save an instance of the StripeAccount model
            stripe_account = StripeAccount.objects.create(
                user=user,
                account_id=account.id,
            )

            # Return a response with the created Stripe account details
            return Response({
                'message': 'Stripe account created successfully',
                'account_id': account.id,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import stripe

class CreateStripeAccountLink(APIView):
    def post(self, request):
        try:
            # Get the authenticated user
            user = request.user

            # Query the database to fetch the StripeAccount associated with the user
            try:
                stripe_account = StripeAccount.objects.get(user=user)
                account_id = stripe_account.account_id
            except StripeAccount.DoesNotExist:
                return Response({'error': 'StripeAccount not found for this user'}, status=404)

            # Create a Stripe account link using the retrieved account_id
            account_link = stripe.AccountLink.create(
                account=account_id,
                refresh_url="https://bnr360.live/freelancer/profile",
                return_url="https://bnr360.live/freelancer/profile",
                type="account_onboarding",
            )

            return Response({'url': account_link.url})
        except Exception as e:
            return Response({'error': str(e)})

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import stripe
from jobpost.models import JobPost

class CreateStripeCheckoutSession(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user
            job_id = request.data.get('job_id')
            if not job_id:
                return Response({'error': 'job_id is required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

            job = get_object_or_404(Payment, job=job_id)
            freelancer= job.freelancer
            # seller= job.freelancer
            # freelancer = seller.user
            print(freelancer)
            price_id=job.price_id
            # Query the database to fetch the StripeAccount associated with the user
            try:
                stripe_account = StripeAccount.objects.get(user=freelancer)
                account_id = stripe_account.account_id
            except StripeAccount.DoesNotExist:
                return Response({'error': 'StripeAccount not found for freelancer'}, status=404)

            # Create a Stripe Checkout Session
            session = stripe.checkout.Session.create(
                mode="payment",
                line_items=[{"price": f'{price_id}', "quantity": 1}],
                payment_intent_data={
                    "application_fee_amount": 123,
                    "transfer_data": {"destination": f'{account_id}'},
                    "metadata": {
                        'payment_id': job.payment_id,
        # Other relevant metadata
                    }
                },
                success_url="https://bnr360.live/client/home",
                cancel_url="https://bnr360.live/client/home",
                )
            job.intent_id = session.payment_intent
            job.save()
            # Determine the status based on the Stripe session status
            response_data = {
            'session_id': session.id,
            'url': session.url,
        }
            return Response(response_data)
        except Exception as e:
            # job.status = 'failed'
            # job.save()
            return Response({'error': str(e)})

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
import stripe

class CreateStripePrice(APIView):
    def post(self, request):
        try:
            # Get the price amount from the request data (you can adapt this to your project's data source)
            price_amount = request.data.get('price_amount')  # Assuming the amount is in cents

            if price_amount is None:
                return Response({'error': 'Price amount is required in the request data.'}, status=400)

            # Create a Stripe Price
            price = stripe.Price.create(
                unit_amount=price_amount,  # The price amount in cents (e.g., $100.00 as 10000 cents)
                currency='usd',  # Replace with the appropriate currency code
                product='your_product_id',  # Replace with your product ID
                # recurring={'interval': 'month'},  # Adjust recurrence as needed
            )

            return Response({'price_id': price.id})
        except Exception as e:
            return Response({'error': str(e)})

from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from jobpost.models import JobPost

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        try:
            # Extract relevant information from the request or perform any necessary logic
            job=request.data.get('job')
            job_obj = JobPost.objects.get(id=job)
    # Now you have the Job object, and you can use it as needed.
        except:
    # Handle the case where the Job with the given ID does not exist
                return Response({"error": f"Job with ID {job} does not exist"}, status=404)
        
        project_budget = job_obj.project_budget
        client_id = job_obj.client
        freelance_id = job_obj.freelancer

            # Your additional logic or data validation here

            # Now, create a new Payment instance with the extracted data
        # try:
        instance = Payment.objects.create(
            amount=project_budget,
            client=client_id,
            freelancer=freelance_id,
            job_id=job
            # Include other relevant fields from request.data
        )

        serializer = self.get_serializer(instance)
        try:
            # pre_save.disconnect(pre_save_payment, sender=Payment)
            # Get the price amount from the instance or request data (adapt as needed)
            price_amount = project_budget  # Assuming the amount is in cents

            if price_amount is None:
                pass
                # Handle the case where the price amount is missing
            # product = stripe.Product.create(
            #     name='hello world',
            #     type='service',  # Replace with 'service' or 'good' as appropriate
            #     # Add other product details as needed
            # )
            price_amount_cents = int(price_amount * 100)
            price = stripe.Price.create(
                unit_amount=price_amount_cents,
                currency='usd',  # Replace with the appropriate currency code
                recurring=None,  # No recurrence for one-time payments
                product_data={
                    'name': 'software',
                    # Add other product data as needed
                }
            )

            # Set the price_id in the payment model
            instance.price_id = price.id
            instance.save()
            # pre_save.connect(pre_save_payment, sender=Payment)
        except Exception as e:
            print(e)
            # Handle any exceptions that may occur during the Stripe Price creation
            pass
        return Response(serializer.data)
        # except Exception as e:
        #     # Handle any exceptions that may occur during the creation process
        #     # print(e)
        #     return Response({"error": "Failed to create payment"}, status=500)


from .serializers import PaymentGetSerializer
class PaymentGetViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentGetSerializer



from django.http import HttpResponse
import json
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from notifications.util import send_client_fail_notification,send_client_success_notification,send_seller_fail_notification,send_seller_success_notification
from .models import Account
from decouple import config
@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers['Stripe-Signature']
    key=config('STRIPE_KEY_WEB_HOOK')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        # Extract relevant information
        intent_id = event['data']['object']['id']
        payment_id =event['data']['object']['metadata'].get('payment_id')
        # print(event)
        print('payment_id',payment_id)        
        # Update the Payment model with the new status and intent_id
        payment = Payment.objects.get(payment_id=payment_id)
        send_seller_success_notification(payment.freelancer,payment.job.job_title)
        send_client_success_notification(payment.client.user,payment.job.job_title)
        # freelancer.account.balance = 
        account = Account.objects.get( user=payment.freelancer)
        # freelancer.account.balance = payment.amount
        account.balance+=payment.amount
        # print(freelancer.account.balance)
        account.save()
        payment.status = 'completed'
        payment.intent_id = intent_id
        payment.save()
    

    elif event['type'] == 'payment_intent.payment_failed':
        payment_id = event['data']['object']['metadata'].get('payment_id')
        payment = Payment.objects.get(payment_id=payment_id)
        send_client_fail_notification(payment.client.user,payment.job.job_title)
        send_seller_fail_notification(payment.freelancer,payment.job.job_title)
        payment.status = 'failed'
        # Similar logic for handling payment failure

    # Other event types can be handled similarly

    return HttpResponse(status=200)
