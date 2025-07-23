from rest_framework import serializers
from .models import Quiz, Question, UserQuiz

#  Quiz serializer
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'time_limit']

#  Question serializer (hide correct_option)
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        exclude = ['correct_option']

#  Used for quiz submission POST data
class SubmitAnswerSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = serializers.DictField(child=serializers.IntegerField())

# Leaderboard or quiz history
class UserQuizSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    taken_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)  # Add this

    class Meta:
        model = UserQuiz
        fields = ['user', 'score', 'taken_on']
