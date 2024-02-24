from django.db import models
from jobpost.models import JobPost
from Seller.models import Seller
class JobProposal(models.Model):

    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='proposals')
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    cover_letter = models.TextField()
    relevant_examples = models.TextField(blank=True)

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

   
from django.db.models.signals import post_save
from django.dispatch import receiver
from Payment.models import Payment
@receiver(post_save, sender=JobProposal)
def deduct_connects_on_proposal_creation(sender, instance, created, **kwargs):
    print('deduct_connects_on_proposal_creation')
    if created:
        # Assuming that JobProposal has a user field related to the user who made the proposal
        seller = instance.seller  # Access the client associated with the JobProposal
        user = seller.user
        try:
            payment = Payment.objects.get(user=user)
        except Exception as e:
            # payment = Payment.objects.create(user=user, amount=250)
            print(e)
            pass
        else:
            if payment.amount >= 8:
                payment.amount -= 8
                payment.save()
