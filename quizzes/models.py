from django.db import models


class Quiz(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=180)
    pass_score = models.PositiveSmallIntegerField(default=70)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    class Type(models.TextChoices):
        MCQ = "mcq", "QCM"
        OPEN = "open", "Question ouverte"

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=Type.choices, default=Type.MCQ)
    points = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.text[:80]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)


class QuizResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(default=0)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
