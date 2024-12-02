import uuid
from django.db import models


class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True)
    referred_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals'
    )

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    def generate_invite_code(self):
        import random
        import string
        return ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6))

    def __str__(self):
        return self.phone_number
