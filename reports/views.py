from django.shortcuts import render
from vendors.models import Vendor
from orders.models import OrderItem
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required

@login_required
def vendor_report(request):
    vendor = request.user.vendor

    # Total de vendas realizadas (entregues)
    total_sales = OrderItem.objects.filter(vendor=vendor, status='DELIVERED') \
                                   .aggregate(total=Sum('price'))['total'] or 0

    # Total de pedidos
    total_orders = OrderItem.objects.filter(vendor=vendor).count()

    # Produtos sem estoque
    out_of_stock = vendor.product_set.filter(stock__lte=0).count()

    # Total de VendorPayout pendentes
    pending_payouts = vendor.vendorpayout_set.filter(status='PENDING') \
                                             .aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'out_of_stock': out_of_stock,
        'pending_payouts': pending_payouts
    }

    return render(request, 'reports/vendor_report.html', context)