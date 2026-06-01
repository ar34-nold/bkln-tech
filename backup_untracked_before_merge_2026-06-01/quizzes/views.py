from django.shortcuts import get_object_or_404, render

from .models import Quiz


def quiz_detail(request, pk):
    return render(request, "quizzes/detail.html", {"quiz": get_object_or_404(Quiz, pk=pk, published=True)})

# Create your views here.
