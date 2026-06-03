import csv
import json
import os
from tempfile import NamedTemporaryFile

from django import forms
from django.contrib import admin, messages
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path

from .models import Chapter, Course, CourseCategory
from lessons.models import Lesson
from courses.management.commands.course_program import Command as CourseProgramCommand


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ("position", "title", "published")


class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "position")
    list_filter = ("course",)
    inlines = [LessonInline]


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 1
    show_change_link = True


class ProgramForm(forms.Form):
    ACTION_CHOICES = (("export", "Exporter"), ("import", "Importer"))
    FORMAT_CHOICES = (("json", "JSON"), ("csv", "CSV"))

    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.RadioSelect)
    format = forms.ChoiceField(choices=FORMAT_CHOICES)
    file = forms.FileField(required=False, help_text="Sélectionnez un fichier JSON ou CSV pour l'import.")
    update = forms.BooleanField(required=False, label="Mettre à jour les éléments existants")


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "trainer", "published", "created_at")
    list_filter = ("published", "category")
    search_fields = ("title", "trainer__username")
    inlines = [ChapterInline]
    change_list_template = "admin/courses/course/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("programs/", self.admin_site.admin_view(self.programs_view), name="courses_course_programs"),
        ]
        return custom_urls + urls

    def programs_view(self, request):
        form = ProgramForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            action = form.cleaned_data["action"]
            fmt = form.cleaned_data["format"]
            update = form.cleaned_data["update"]
            if action == "export":
                return self.export_programs(fmt)
            if action == "import":
                uploaded_file = form.cleaned_data["file"]
                if not uploaded_file:
                    messages.error(request, "Veuillez sélectionner un fichier pour l'import.")
                else:
                    return self.import_programs(request, uploaded_file, fmt, update)
        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "form": form,
            "title": "Import/Export des programmes",
        }
        return TemplateResponse(request, "admin/courses/course/programs.html", context)

    def export_programs(self, fmt):
        command = CourseProgramCommand()
        data = command.build_export_data()
        if fmt == "json":
            content = json.dumps(data, ensure_ascii=False, indent=2)
            response = HttpResponse(content, content_type="application/json")
            response["Content-Disposition"] = "attachment; filename=course_programs.json"
            return response
        output = []
        for course in data["courses"]:
            for chapter in course["chapters"]:
                if chapter["lessons"]:
                    for lesson in chapter["lessons"]:
                        output.append({
                            "course_slug": course["slug"],
                            "course_title": course["title"],
                            "course_category_slug": course["category_slug"],
                            "course_category_name": course["category_name"],
                            "course_description": course["description"],
                            "course_price": course["price"],
                            "course_published": course["published"],
                            "course_trainer": course["trainer"],
                            "chapter_position": chapter["position"],
                            "chapter_title": chapter["title"],
                            "lesson_position": lesson["position"],
                            "lesson_title": lesson["title"],
                            "lesson_video_url": lesson["video_url"],
                            "lesson_pdf": lesson["pdf"],
                            "lesson_content": lesson["content"],
                            "lesson_published": lesson["published"],
                        })
                else:
                    output.append({
                        "course_slug": course["slug"],
                        "course_title": course["title"],
                        "course_category_slug": course["category_slug"],
                        "course_category_name": course["category_name"],
                        "course_description": course["description"],
                        "course_price": course["price"],
                        "course_published": course["published"],
                        "course_trainer": course["trainer"],
                        "chapter_position": chapter["position"],
                        "chapter_title": chapter["title"],
                        "lesson_position": "",
                        "lesson_title": "",
                        "lesson_video_url": "",
                        "lesson_pdf": "",
                        "lesson_content": "",
                        "lesson_published": "",
                    })
        csv_file = NamedTemporaryFile(delete=False, suffix=".csv")
        try:
            with open(csv_file.name, "w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=command.CSV_HEADERS)
                writer.writeheader()
                writer.writerows(output)
            with open(csv_file.name, "r", encoding="utf-8") as file:
                response = HttpResponse(file.read(), content_type="text/csv")
                response["Content-Disposition"] = "attachment; filename=course_programs.csv"
                return response
        finally:
            os.unlink(csv_file.name)

    def import_programs(self, request, uploaded_file, fmt, update):
        command = CourseProgramCommand()
        suffix = ".json" if fmt == "json" else ".csv"
        temp_file = NamedTemporaryFile(delete=False, suffix=suffix)
        try:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_file.close()
            data = command.read_file(temp_file.name, fmt)
            command.import_data(data, update=update)
            messages.success(request, "Importation terminée avec succès.")
        finally:
            os.unlink(temp_file.name)
        return None


admin.site.register(CourseCategory)
admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)

