from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Quiz
from django.conf import settings

import random
from django.core.mail import send_mail
from .models import PasswordResetOTP
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm


# ----------------------------
# User Registration View
# ----------------------------
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('quiz-list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# ----------------------------
# User Login View
# ----------------------------
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Handle "Remember Me"
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)  # Expires on browser close
            else:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)  # Default: 2 weeks

            return redirect(request.GET.get('next', 'quiz-list'))  # Redirect to original page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# ----------------------------
# Logout View
# ----------------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------------
# Quiz List Page (Login Required)
# ----------------------------
@login_required
def quiz_list_view(request):
    return render(request, 'quizzes.html')


# ----------------------------
# Start Quiz Page (Login Required)
# ----------------------------
@login_required
def quiz_start_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz_start.html', {'quiz_id': quiz.id})


# ----------------------------
# Leaderboard Page (Login Required)
# ----------------------------
@login_required
def leaderboard_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'leaderboard.html', {'quiz_id': quiz.id})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            PasswordResetOTP.objects.create(user=user, otp=otp)

            send_mail(
                'Your OTP for Password Reset',
                f'Use this OTP to reset your password: {otp}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            request.session['reset_user'] = user.id
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'Email not found')
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        new_password = request.POST['password']
        user_id = request.session.get('reset_user')
        if user_id:
            user = User.objects.get(id=user_id)
            otp_record = PasswordResetOTP.objects.filter(user=user).last()
            if otp_record and not otp_record.is_expired() and otp_record.otp == entered_otp:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully!')
                return redirect('login')
            else:
                messages.error(request, 'Invalid or expired OTP')
    return render(request, 'verify_otp.html')
