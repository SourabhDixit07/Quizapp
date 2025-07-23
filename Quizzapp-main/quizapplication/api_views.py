from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from .models import Quiz, Question, UserQuiz
from .serializers import QuizSerializer, QuestionSerializer, SubmitAnswerSerializer, UserQuizSerializer

# ✅ ViewSet for Django REST Router
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Get all quizzes
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_quizzes(request):
    quizzes = Quiz.objects.all()
    serializer = QuizSerializer(quizzes, many=True)
    return Response(serializer.data)

# ✅ Get questions for a specific quiz
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_quiz_questions(request, quiz_id):
    try:
        questions = Question.objects.filter(quiz_id=quiz_id)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

# ✅ Submit quiz answers and save score
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_answers(request):
    serializer = SubmitAnswerSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        quiz_id = data['quiz_id']
        answers = data['answers']

        questions = Question.objects.filter(quiz_id=quiz_id)
        score = 0
        total = questions.count()
        results = []

        for q in questions:
            selected = answers.get(str(q.id))
            is_correct = selected and int(selected) == q.correct_option
            if is_correct:
                score += 1

            results.append({
                'question': q.text,
                'selected': selected,
                'correct': q.correct_option,
                'correct_option_text': getattr(q, f"option{q.correct_option}")
            })

        UserQuiz.objects.create(
            user=request.user,
            quiz_id=quiz_id,
            score=score
        )

        return Response({
            'score': score,
            'total': total,
            'details': results
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Leaderboard (Top 10 scores)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def leaderboard(request, quiz_id):
    try:
        top_users = UserQuiz.objects.filter(quiz_id=quiz_id).order_by('-score', 'submitted_at')[:10]
        serializer = UserQuizSerializer(top_users, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
