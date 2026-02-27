from django.shortcuts import render, redirect
from orders.models import Order, OrderItem
from products.models import Product

def checkout(request):
    # Para simplificar: pegar todos os produtos adicionados ao carrinho (exemplo)
    cart_items = Product.objects.filter(pk__in=[1,2])  # exemplo, substituir pelo carrinho real
    total = sum([p.price for p in cart_items])
    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total})


    
#===============================================================================#
from django.shortcuts import render, redirect
from orders.models import CartItem, Order, OrderItem, VendorPayout
from products.models import Product
from vendors.models import Vendor
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum([item.subtotal() for item in cart_items])
    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    item = CartItem.objects.get(id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart')    



# Checkout e Criação de Pedidos
#========================================================================#
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('product_list')

    total_amount = sum([item.subtotal() for item in cart_items])

    # Criar pedido geral
    order = Order.objects.create(
        customer=request.user,
        total_amount=total_amount,
        status='PENDING',
        payment_method='PIX/Stripe'  # placeholder
    )

    # Criar OrderItems e VendorPayouts
    vendor_dict = {}
    for item in cart_items:
        order_item = OrderItem.objects.create(
            order=order,
            product=item.product,
            vendor=item.product.vendor,
            quantity=item.quantity,
            price=item.subtotal(),
            status='PENDING'
        )
        # Organizar por vendedor para VendorPayout
        if item.product.vendor not in vendor_dict:
            vendor_dict[item.product.vendor] = []
        vendor_dict[item.product.vendor].append(order_item)
        # Atualizar estoque
        item.product.stock -= item.quantity
        item.product.save()

    # Criar registros de pagamento para cada vendedor
    for vendor, items in vendor_dict.items():
        total_vendor = sum([oi.price for oi in items])
        commission = total_vendor * 0.1  # Exemplo: 10% comissão
        payout = VendorPayout.objects.create(
            vendor=vendor,
            total_amount=total_vendor,
            commission=commission,
            status='PENDING'
        )
        payout.order_items.set(items)

    # Limpar carrinho
    cart_items.delete()

    return render(request, 'orders/checkout_success.html', {'order': order})

# Atualização de Pedidos como "Pago" Manualmente
#========================================================================#
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order, OrderItem, VendorPayout
from django.contrib.auth.decorators import login_required

@login_required
def mark_order_paid(request, order_id):
    # Marca o pedido inteiro como pago manualmente
    order = get_object_or_404(Order, id=order_id)
    order.status = 'PAID'
    order.save()

    # Atualiza todos os itens do pedido
    order_items = order.items.all()
    for item in order_items:
        item.status = 'PAID'
        item.save()

    # Atualiza os VendorPayouts correspondentes
    payouts = VendorPayout.objects.filter(order_items__in=order_items).distinct()
    for payout in payouts:
        payout.status = 'PENDING'  # ainda não pago ao vendedor
        payout.save()

    return redirect('view_order', order_id=order.id)
