from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # img = 
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.CharField(blank=True, max_length=500)
    location = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return f'Profile for {self.user.username}'
    