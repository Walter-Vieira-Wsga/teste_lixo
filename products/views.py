from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from products.forms import ProductForm
from django.db.models import Prefetch
from products.models import Product, Category, ProductImage
from django.contrib.auth.mixins import LoginRequiredMixin

# Listagem de produtos ativos
class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.filter(is_main=True),
                to_attr="main_images"
            )
        )

# Detalhes do produto via slug
class ProductDetailSlugView(DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Product, slug=slug, active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["related_products"] = Product.objects.filter(
            category=self.object.category,
            active=True
        ).exclude(id=self.object.id)[:4]

        return context

# Criar produto (só para vendedores logados)
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"

    def form_valid(self, form):
        product = form.save(commit=False)
        product.vendor = self.request.user.vendor  # assume que usuário tem FK para Vendor
        product.save()
        return redirect('vendor_dashboard')