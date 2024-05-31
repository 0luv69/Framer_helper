from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.email import send_account_activation_email


# Create your models here.
class Profile(models.Model):
    user_m = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank= True)
    is_framer = models.BooleanField(default=0)
    def __str__(self):
        return str(self.user_m)

class FramerUser(models.Model):
    Profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='frameruser')
    Bio= models.TextField(default='Hey, I am Framer Here')
    profile_img = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    ph_num = models.IntegerField(null=True,  blank=True)
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    trust_rate = models.IntegerField(choices=RATING_CHOICES, default=1)
    def __str__(self):
        return f"{self.Profile.user_m} as framer"

class BuyerUser(models.Model):
    Profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='buyeruser')
    profile_img = models.ImageField(upload_to='profile_pic', null=True, blank=True)
    ph_num = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.Profile.user_m} as User"






@receiver(post_save, sender= User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            email = instance.email 
            Profile.objects.create(user_m= instance, email_token=email_token )
            send_account_activation_email(email, email_token, instance)
    except Exception as E:
        print(E)