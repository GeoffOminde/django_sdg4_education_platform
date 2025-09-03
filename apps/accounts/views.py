from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction

from .models import User, AIInteraction
from .forms import UserRegistrationForm


def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    user.credits = 10  # Welcome credits
                    user.save()
                    
                    # Auto-login
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password1')
                    user = authenticate(username=user.email, password=password)
                    login(request, user)
                    
                    messages.success(request, 'Registration successful! You have 10 free credits to start.')
                    return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'Registration failed. Please try again.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard_view(request):
    """User dashboard"""
    recent_interactions = AIInteraction.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'user': request.user,
        'recent_interactions': recent_interactions,
    }
    return render(request, 'dashboard.html', context)


@login_required
@require_http_methods(["GET"])
def user_stats_api(request):
    """API endpoint for user statistics"""
    total_interactions = AIInteraction.objects.filter(user=request.user).count()
    
    return JsonResponse({
        'credits': request.user.credits,
        'total_interactions': total_interactions,
        'username': request.user.username
    })

