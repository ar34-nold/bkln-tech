from django.conf import settings
from django.db import models


class BlogCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name="articles")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blog/", blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=120)
    author_email = models.EmailField()
    message = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
