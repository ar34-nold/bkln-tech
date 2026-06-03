from django.http import JsonResponse

from blog.models import Article
from courses.models import Course
from products.models import Product


def api_home(request):
    return JsonResponse({
        "name": "BKLN-TECH API",
        "resources": ["products", "courses", "articles"],
    })


def api_products(request):
    data = list(Product.objects.filter(active=True).values("id", "name", "sku", "price", "stock", "category__name"))
    return JsonResponse({"results": data})


def api_courses(request):
    data = list(Course.objects.filter(published=True).values("id", "title", "price", "category__name", "trainer__username"))
    return JsonResponse({"results": data})


def api_articles(request):
    data = list(Article.objects.filter(published=True).values("id", "title", "slug", "excerpt", "category__name"))
    return JsonResponse({"results": data})
