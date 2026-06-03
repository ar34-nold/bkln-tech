from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class ProductPagesTests(TestCase):
    def test_product_catalog_loads(self):
        category = Category.objects.create(name="Ordinateurs", slug="ordinateurs")
        Product.objects.create(category=category, name="PC Test", slug="pc-test", sku="PC-001", description="Test", price=1000, stock=1)
        response = self.client.get(reverse("product_list"))
        self.assertContains(response, "PC Test")
