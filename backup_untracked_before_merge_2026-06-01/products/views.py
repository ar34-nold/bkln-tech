from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request):
    products = Product.objects.filter(active=True).select_related("category")
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(sku__icontains=query))
    if category:
        products = products.filter(category__slug=category)
    return render(request, "products/list.html", {"products": products, "categories": Category.objects.all(), "query": query})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, "products/detail.html", {"product": product})

# Create your views here.
