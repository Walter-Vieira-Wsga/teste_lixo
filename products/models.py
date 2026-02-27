from django.db import models
from vendors.models import Vendor

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # 👈 ADICIONAR
    description = models.TextField(blank=True)
    ncm = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()    
    
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/images/")
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem de {self.product.name}"    
    
