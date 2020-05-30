from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # img = 
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.CharField(blank=True, max_length=500)
    location = models.CharField(blank=True, max_length=50)
    email = models.EmailField(unique=True, max_length=200)

    def __str__(self):
        return f'Profile for {self.user.username}'

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()