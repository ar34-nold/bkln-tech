from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from courses.models import Course

from .models import Enrollment


@login_required
def student_space(request):
    return render(request, "academy/student.html", {"enrollments": Enrollment.objects.filter(student=request.user), "courses": Course.objects.filter(published=True)[:6]})

# Create your views here.
