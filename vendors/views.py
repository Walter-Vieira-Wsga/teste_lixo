from django.shortcuts import render, redirect
from vendors.forms import VendorForm
from vendors.models import Vendor

def vendor_register(request):
    if request.method == 'POST':
        form = VendorForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.save()
            return redirect('vendor_dashboard')
    else:
        form = VendorForm()
    return render(request, 'vendors/vendor_register.html', {'form': form})

#----------------------------------------------------------------------------#
from products.models import Product
from orders.models import OrderItem
from django.db.models import Sum

def vendor_dashboard(request):
    vendor = request.user.vendor
    products_count = Product.objects.filter(vendor=vendor).count()
    orders_count = OrderItem.objects.filter(vendor=vendor).count()
    total_sales = OrderItem.objects.filter(vendor=vendor, status='DELIVERED').aggregate(total=Sum('price'))['total'] or 0
    return render(request, 'vendors/dashboard.html', {
        'products_count': products_count,
        'orders_count': orders_count,
        'total_sales': total_sales
    })
