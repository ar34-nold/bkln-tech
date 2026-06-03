from django.contrib import admin

from .models import Choice, Question, Quiz, QuizResult

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizResult)

# Register your models here.
