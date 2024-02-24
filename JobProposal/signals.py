# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from Payment.models import Account
# from .models import JobProposal
# @receiver(post_save, sender=JobProposal)
# def deduct_connects_on_proposal_creation(sender, instance, created, **kwargs):
#     print('deduct_connects_on_proposal_creation')
#     if created:
#         # Assuming that JobProposal has a user field related to the user who made the proposal
#         client = instance.client  # Access the client associated with the JobProposal
#         user = client.user
#         try:
#             account = Account.objects.get(user=user)
#         except Exception as e:
#             # payment = Payment.objects.create(user=user, amount=250)
#             print(e)
#             pass
#         else:
#             if account.connects >= 8:
#                 account.connects -= 8
#                 account.save()
