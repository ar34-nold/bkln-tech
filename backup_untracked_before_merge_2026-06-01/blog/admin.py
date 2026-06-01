from django.contrib import admin

from .models import Article, BlogCategory, Comment

admin.site.register(BlogCategory)
admin.site.register(Article)
admin.site.register(Comment)

# Register your models here.
