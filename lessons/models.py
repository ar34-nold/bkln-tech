from django.db import models


class Lesson(models.Model):
    chapter = models.ForeignKey("courses.Chapter", on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=180)
    video_url = models.URLField(blank=True)
    pdf = models.FileField(upload_to="academy/lessons/pdf/", blank=True)
    content = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=1)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title


class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="exercises")
    title = models.CharField(max_length=180)
    instructions = models.TextField()
    correction = models.TextField(blank=True)

    def __str__(self):
        return self.title

# Create your models here.
