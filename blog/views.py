from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Article, BlogCategory, Comment


def article_list(request):
    articles = Article.objects.filter(published=True).select_related("category", "author")
    query = request.GET.get("q", "")
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query))
    return render(request, "blog/list.html", {"articles": articles, "categories": BlogCategory.objects.all(), "query": query})


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)
    if request.method == "POST":
        Comment.objects.create(
            article=article,
            author_name=request.POST.get("author_name", ""),
            author_email=request.POST.get("author_email", ""),
            message=request.POST.get("message", ""),
        )
        return redirect("article_detail", slug=slug)
    return render(request, "blog/detail.html", {"article": article})

# Create your views here.
