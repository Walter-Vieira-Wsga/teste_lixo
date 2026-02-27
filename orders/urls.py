from django.urls import path
from orders import views

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]

from orders import views
from django.urls import path


#== (adicionar a marcação manual de pagamento) ==#
urlpatterns = [
    # ... outras rotas
    path('order/<int:order_id>/mark_paid/', views.mark_order_paid, name='mark_order_paid'),
]