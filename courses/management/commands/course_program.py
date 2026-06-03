import csv
import json
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from courses.models import Course, CourseCategory
from lessons.models import Lesson

User = get_user_model()

CSV_HEADERS = [
    "course_slug",
    "course_title",
    "course_category_slug",
    "course_category_name",
    "course_description",
    "course_price",
    "course_published",
    "course_trainer",
    "chapter_position",
    "chapter_title",
    "lesson_position",
    "lesson_title",
    "lesson_video_url",
    "lesson_pdf",
    "lesson_content",
    "lesson_published",
]


def bool_value(value):
    return str(value).strip().lower() in ("1", "true", "yes", "y", "t")


class Command(BaseCommand):
    help = "Import or export course programs from/to JSON or CSV files."

    def add_arguments(self, parser):
        parser.add_argument(
            "--export",
            dest="export",
            action="store_true",
            help="Export course programs to a file.",
        )
        parser.add_argument(
            "--import",
            dest="import_",
            action="store_true",
            help="Import course programs from a file.",
        )
        parser.add_argument(
            "--file",
            dest="file_path",
            required=True,
            help="Path to the input or output file.",
        )
        parser.add_argument(
            "--course",
            dest="course_slug",
            help="Optional course slug to export or import a single course.",
        )
        parser.add_argument(
            "--update",
            dest="update",
            action="store_true",
            help="Update existing courses, chapters and lessons when importing.",
        )

    def handle(self, *args, **options):
        export = options["export"]
        import_ = options["import_"]
        file_path = options["file_path"]
        course_slug = options.get("course_slug")
        update = options.get("update", False)

        if export == import_:
            raise CommandError("Specify exactly one of --export or --import.")

        fmt = self.detect_format(file_path)
        if fmt not in ("json", "csv"):
            raise CommandError("Unsupported file format. Use .json or .csv.")

        if export:
            self.stdout.write(f"Exporting programs to {file_path} ({fmt})...")
            data = self.build_export_data(course_slug)
            if fmt == "json":
                self.write_json(file_path, data)
            else:
                self.write_csv(file_path, data)
            self.stdout.write(self.style.SUCCESS("Export completed."))
        else:
            self.stdout.write(f"Importing programs from {file_path} ({fmt})...")
            data = self.read_file(file_path, fmt)
            self.import_data(data, update=update)
            self.stdout.write(self.style.SUCCESS("Import completed."))

    def detect_format(self, path):
        _, ext = os.path.splitext(path.lower())
        if ext == ".json":
            return "json"
        if ext == ".csv":
            return "csv"
        return None

    def build_export_data(self, course_slug=None):
        courses = Course.objects.filter(published=True)
        if course_slug:
            courses = courses.filter(slug=course_slug)

        result = []
        for course in courses.select_related("category", "trainer").prefetch_related("chapters__lessons"):
            item = {
                "category_slug": course.category.slug,
                "category_name": course.category.name,
                "title": course.title,
                "slug": course.slug,
                "description": course.description,
                "price": str(course.price),
                "published": course.published,
                "trainer": course.trainer.username,
                "chapters": [],
            }
            for chapter in course.chapters.all():
                chapter_item = {
                    "title": chapter.title,
                    "position": chapter.position,
                    "lessons": [],
                }
                for lesson in chapter.lessons.all():
                    chapter_item["lessons"].append(
                        {
                            "title": lesson.title,
                            "position": lesson.position,
                            "video_url": lesson.video_url,
                            "pdf": lesson.pdf.name if lesson.pdf else "",
                            "content": lesson.content,
                            "published": lesson.published,
                        }
                    )
                item["chapters"].append(chapter_item)
            result.append(item)
        return {"courses": result}

    def write_json(self, path, data):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def write_csv(self, path, data):
        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for course in data["courses"]:
                for chapter in course["chapters"]:
                    if chapter["lessons"]:
                        for lesson in chapter["lessons"]:
                            writer.writerow(
                                {
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
                                }
                            )
                    else:
                        writer.writerow(
                            {
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
                            }
                        )

    def read_file(self, path, fmt):
        if fmt == "json":
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        with open(path, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != CSV_HEADERS:
                raise CommandError("CSV file header does not match expected format.")
            courses = {}
            for row in reader:
                slug = row["course_slug"].strip()
                if not slug:
                    continue
                course = courses.setdefault(slug, {
                    "category_slug": row["course_category_slug"].strip(),
                    "category_name": row["course_category_name"].strip(),
                    "title": row["course_title"].strip(),
                    "slug": slug,
                    "description": row["course_description"].strip(),
                    "price": row["course_price"].strip(),
                    "published": bool_value(row["course_published"]),
                    "trainer": row["course_trainer"].strip(),
                    "chapters": {},
                })
                chapter_key = f"{row['chapter_position']}_{row['chapter_title'].strip()}"
                if chapter_key not in course["chapters"]:
                    course["chapters"][chapter_key] = {
                        "title": row["chapter_title"].strip(),
                        "position": int(row["chapter_position"] or 0),
                        "lessons": [],
                    }
                if row["lesson_title"].strip():
                    course["chapters"][chapter_key]["lessons"].append(
                        {
                            "title": row["lesson_title"].strip(),
                            "position": int(row["lesson_position"] or 0),
                            "video_url": row["lesson_video_url"].strip(),
                            "pdf": row["lesson_pdf"].strip(),
                            "content": row["lesson_content"].strip(),
                            "published": bool_value(row["lesson_published"]),
                        }
                    )
            for course in courses.values():
                course["chapters"] = list(course["chapters"].values())
            return {"courses": list(courses.values())}

    def import_data(self, data, update=False):
        for course_data in data.get("courses", []):
            category, _ = CourseCategory.objects.get_or_create(
                slug=course_data["category_slug"],
                defaults={"name": course_data["category_name"]},
            )
            trainer = User.objects.filter(username=course_data["trainer"]).first()
            if not trainer:
                raise CommandError(f"Trainer user '{course_data['trainer']}' not found.")
            course, created = Course.objects.get_or_create(
                slug=course_data["slug"],
                defaults={
                    "category": category,
                    "trainer": trainer,
                    "title": course_data["title"],
                    "description": course_data.get("description", ""),
                    "price": course_data.get("price", 0),
                    "published": course_data.get("published", False),
                },
            )
            if not created and update:
                course.title = course_data["title"]
                course.description = course_data.get("description", "")
                course.price = course_data.get("price", 0)
                course.published = course_data.get("published", False)
                course.category = category
                course.trainer = trainer
                course.save()

            chapter_lookup = {}
            for chapter_data in course_data.get("chapters", []):
                chapter, chapter_created = course.chapters.get_or_create(
                    title=chapter_data["title"],
                    defaults={"position": chapter_data.get("position", 0)},
                )
                if not chapter_created and update:
                    chapter.position = chapter_data.get("position", 0)
                    chapter.save()
                chapter_lookup[chapter_data["title"]] = chapter

                for lesson_data in chapter_data.get("lessons", []):
                    lesson, lesson_created = Lesson.objects.get_or_create(
                        chapter=chapter,
                        title=lesson_data["title"],
                        defaults={
                            "position": lesson_data.get("position", 0),
                            "video_url": lesson_data.get("video_url", ""),
                            "pdf": lesson_data.get("pdf", ""),
                            "content": lesson_data.get("content", ""),
                            "published": lesson_data.get("published", False),
                        },
                    )
                    if not lesson_created and update:
                        lesson.position = lesson_data.get("position", 0)
                        lesson.video_url = lesson_data.get("video_url", "")
                        lesson.content = lesson_data.get("content", "")
                        lesson.published = lesson_data.get("published", False)
                        lesson.save()
