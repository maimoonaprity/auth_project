from django.db import models
from django.conf import settings 
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone



class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    access_duration = models.DurationField()
    is_valid = models.BooleanField(default=True)
 

   
    def access_end(self):
        """Return the datetime when access expires"""
        return self.created_at + self.access_duration
    
    def check_validity(self):
        """Check if the user is still within access period."""
        now = timezone.now()
        if now <= self.access_end:
            self.is_valid = True
        else:
            self.is_valid = False
        self.save(update_fields=['is_valid'])
        return self.is_valid

class Profile(models.Model):
   
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
  