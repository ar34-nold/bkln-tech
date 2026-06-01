from django.contrib import admin

from .models import Chapter, Course, CourseCategory

admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(Chapter)

# Register your models here.
