from django.shortcuts import get_object_or_404, render

from .models import Lesson


def lesson_detail(request, pk):
    return render(request, "lessons/detail.html", {"lesson": get_object_or_404(Lesson, pk=pk, published=True)})

# Create your views here.
