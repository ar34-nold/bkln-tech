from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, CourseCategory
from academy.models import Enrollment


def course_list(request):
    courses = Course.objects.filter(published=True).select_related("category", "trainer")
    category = request.GET.get("category")
    if category:
        courses = courses.filter(category__slug=category)
    return render(request, "courses/list.html", {"courses": courses, "categories": CourseCategory.objects.all()})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, published=True)
    return render(request, "courses/detail.html", {"course": course})


@login_required
def course_enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, published=True)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, "Votre demande d'inscription a été enregistrée. Nous vous contacterons bientôt.")
    else:
        messages.info(request, "Vous êtes déjà inscrit(e) à cette formation.")
    return redirect('academy_home')

# Create your views here.
