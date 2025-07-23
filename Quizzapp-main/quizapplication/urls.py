from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

# DRF router setup
router = DefaultRouter()
router.register(r'quizzes', api_views.QuizViewSet, basename='quiz')

urlpatterns = [
    #  Homepage shows quiz list
    path('', views.quiz_list_view, name='home'),

    # Template Views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('quizzes/', views.quiz_list_view, name='quiz-list'),
    path('quiz/<int:quiz_id>/start/', views.quiz_start_view, name='quiz-start'),
    path('leaderboard/<int:quiz_id>/', views.leaderboard_view, name='leaderboard'),

    # Custom API endpoints
    path('api/quiz/<int:quiz_id>/questions/', api_views.get_quiz_questions),
    path('api/submit/', api_views.submit_answers),
    path('api/leaderboard/<int:quiz_id>/', api_views.leaderboard),

    # DRF Router-based API
    path('api/', include(router.urls)),
]
