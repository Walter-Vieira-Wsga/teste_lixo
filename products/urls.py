from django.urls import path
from .views import ProductListView, ProductDetailSlugView, ProductCreateView

app_name = "products"

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<slug:slug>/', ProductDetailSlugView.as_view(), name='product_detail'),
    
]