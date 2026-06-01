import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from products.models import Product

from .models import Order, OrderItem


@login_required
def order_list(request):
    return render(request, "generic/list.html", {"title": "Commandes", "objects": Order.objects.filter(user=request.user), "fields": ["reference", "status", "created_at"]})


@login_required
def quick_order(request, product_id):
    product = Product.objects.get(pk=product_id)
    order = Order.objects.create(
        user=request.user,
        reference=f"BK-{uuid.uuid4().hex[:10].upper()}",
        full_name=request.user.get_full_name() or request.user.username,
        phone=request.POST.get("phone", ""),
        address=request.POST.get("address", ""),
        payment_method=request.POST.get("payment_method", "mobile_money"),
        payment_target="72 34 37 76",
        payment_reference=request.POST.get("payment_reference", ""),
    )
    OrderItem.objects.create(order=order, product=product, quantity=int(request.POST.get("quantity", 1)), unit_price=product.current_price)
    return redirect("order_list")

# Create your views here.
