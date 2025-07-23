from django.contrib import admin
from .models import Quiz, Question, UserQuiz


class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'time_limit']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'text']

class UserQuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quiz', 'score', 'submitted_at']  

# Register with the admin site
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserQuiz, UserQuizAdmin)
