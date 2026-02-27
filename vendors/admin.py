from django.contrib import admin
from .models import Vendor

class VendorAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'cnpj', 'description','is_approved']  # remove 'slug'

admin.site.register(Vendor, VendorAdmin)
