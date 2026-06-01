from django.shortcuts import get_object_or_404, render

from .models import Course, CourseCategory


def course_list(request):
    courses = Course.objects.filter(published=True).select_related("category", "trainer")
    category = request.GET.get("category")
    if category:
        courses = courses.filter(category__slug=category)
    return render(request, "courses/list.html", {"courses": courses, "categories": CourseCategory.objects.all()})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, published=True)
    return render(request, "courses/detail.html", {"course": course})

# Create your views here.
