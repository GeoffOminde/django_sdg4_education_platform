from django.urls import path
from . import views

app_name = 'ai_tutor'

urlpatterns = [
    path('tutor/', views.ai_tutor, name='tutor'),
    path('explain/', views.explain_concept, name='explain'),
    path('generate-quiz/', views.generate_quiz, name='generate_quiz'),
]

