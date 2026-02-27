from django.db import models
from django.conf import settings

class Vendor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor'
    )
    company_name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    logo = models.ImageField(upload_to='vendors/logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.company_name