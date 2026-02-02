from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    access_duration = models.DurationField(default=timedelta(seconds=24))
    is_valid = models.BooleanField(default=True)

    def check_validity(self):
        """Check if the user is still within the allowed access duration."""
        now = timezone.now()
        access_end = self.created_at + self.access_duration
        self.is_valid = self.created_at <= now <= access_end
        self.save(update_fields=['is_valid'])
        return self.is_valid