import json
import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import transaction
from django_ratelimit.decorators import ratelimit

from apps.accounts.models import User, AIInteraction


class PromptTemplates:
    """Educational prompt templates for different learning scenarios"""
    
    TUTOR_SYSTEM = """You are an expert educational tutor aligned with SDG 4 (Quality Education). 
    Provide clear, accurate, and encouraging responses. Adapt your explanations to the user's level.
    Focus on understanding rather than memorization. Use examples and analogies when helpful."""
    
    EXPLAIN_CONCEPT = """Explain the concept of "{topic}" in a way that's appropriate for {level} level students. 
    Include:
    1. A clear definition
    2. Why it's important
    3. A real-world example
    4. Common misconceptions to avoid
    
    Topic: {topic}
    Student Level: {level}
    Additional Context: {context}"""
    
    QUIZ_GENERATOR = """Create a {difficulty} level quiz about "{topic}" with {num_questions} questions.
    Format as JSON with this structure:
    {{"questions": [{{"question": "...", "options": ["A", "B", "C", "D"], "correct": "A", "explanation": "..."}}]}}
    
    Topic: {topic}
    Difficulty: {difficulty}
    Number of questions: {num_questions}"""


def query_huggingface(prompt, model=None):
    """Query Hugging Face Inference API"""
    if not settings.HUGGINGFACE_API_TOKEN:
        raise ValueError("Hugging Face API token not configured")
    
    model = model or settings.HUGGINGFACE_MODEL
    
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True
        }
    }
    
    url = f"https://api-inference.huggingface.co/models/{model}"
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', '').strip()
        elif isinstance(result, dict):
            return result.get('generated_text', '').strip()
        else:
            return "I apologize, but I couldn't generate a proper response. Please try again."
            
    except requests.exceptions.RequestException as e:
        raise Exception("AI service temporarily unavailable")


@login_required
@require_http_methods(["POST"])
@ratelimit(key='user', rate='10/m', method='POST')
def ai_tutor(request):
    """AI tutoring endpoint with prompt engineering"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if 'question' not in data:
        return JsonResponse({'error': 'Question is required'}, status=400)
    
    question = data['question'].strip()
    if not question:
        return JsonResponse({'error': 'Question cannot be empty'}, status=400)
    
    # Check credits
    if request.user.credits < 1:
        return JsonResponse({'error': 'Insufficient credits. Please purchase more credits.'}, status=402)
    
    try:
        with transaction.atomic():
            # Deduct credits
            user = User.objects.select_for_update().get(id=request.user.id)
            if not user.deduct_credits(1):
                return JsonResponse({'error': 'Insufficient credits'}, status=402)
            
            # Construct educational prompt
            educational_prompt = f"""{PromptTemplates.TUTOR_SYSTEM}

Student Question: {question}

Please provide a helpful, educational response that promotes understanding and learning."""
            
            # Query AI
            try:
                ai_response = query_huggingface(educational_prompt)
                
                # Save interaction
                interaction = AIInteraction.objects.create(
                    user=user,
                    prompt=question,
                    response=ai_response,
                    model_used=settings.HUGGINGFACE_MODEL,
                    credits_used=1
                )
                
                return JsonResponse({
                    'response': ai_response,
                    'credits_remaining': user.credits,
                    'interaction_id': interaction.id
                })
                
            except Exception as e:
                # Refund credits on AI failure
                user.add_credits(1)
                return JsonResponse({'error': 'AI service error. Credits refunded.'}, status=500)
                
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)


@login_required
@require_http_methods(["POST"])
@ratelimit(key='user', rate='5/m', method='POST')
def explain_concept(request):
    """Explain educational concepts with structured prompts"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    required_fields = ['topic', 'level']
    if not all(field in data for field in required_fields):
        return JsonResponse({'error': 'Topic and level are required'}, status=400)
    
    if request.user.credits < 2:  # Explanations cost 2 credits
        return JsonResponse({'error': 'Insufficient credits (2 required)'}, status=402)
    
    try:
        with transaction.atomic():
            user = User.objects.select_for_update().get(id=request.user.id)
            if not user.deduct_credits(2):
                return JsonResponse({'error': 'Insufficient credits'}, status=402)
            
            # Use structured prompt template
            prompt = PromptTemplates.EXPLAIN_CONCEPT.format(
                topic=data['topic'],
                level=data.get('level', 'beginner'),
                context=data.get('context', 'general education')
            )
            
            try:
                ai_response = query_huggingface(prompt)
                
                interaction = AIInteraction.objects.create(
                    user=user,
                    prompt=f"Explain: {data['topic']} ({data['level']} level)",
                    response=ai_response,
                    model_used=settings.HUGGINGFACE_MODEL,
                    credits_used=2
                )
                
                return JsonResponse({
                    'explanation': ai_response,
                    'credits_remaining': user.credits,
                    'topic': data['topic'],
                    'level': data['level']
                })
                
            except Exception as e:
                user.add_credits(2)  # Refund
                return JsonResponse({'error': 'AI service error. Credits refunded.'}, status=500)
                
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)


@login_required
@require_http_methods(["POST"])
@ratelimit(key='user', rate='3/m', method='POST')
def generate_quiz(request):
    """Generate educational quizzes"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if 'topic' not in data:
        return JsonResponse({'error': 'Topic is required'}, status=400)
    
    if request.user.credits < 3:  # Quiz generation costs 3 credits
        return JsonResponse({'error': 'Insufficient credits (3 required)'}, status=402)
    
    try:
        with transaction.atomic():
            user = User.objects.select_for_update().get(id=request.user.id)
            if not user.deduct_credits(3):
                return JsonResponse({'error': 'Insufficient credits'}, status=402)
            
            prompt = PromptTemplates.QUIZ_GENERATOR.format(
                topic=data['topic'],
                difficulty=data.get('difficulty', 'medium'),
                num_questions=min(int(data.get('num_questions', 5)), 10)  # Max 10 questions
            )
            
            try:
                ai_response = query_huggingface(prompt)
                
                interaction = AIInteraction.objects.create(
                    user=user,
                    prompt=f"Quiz: {data['topic']} ({data.get('difficulty', 'medium')})",
                    response=ai_response,
                    model_used=settings.HUGGINGFACE_MODEL,
                    credits_used=3
                )
                
                return JsonResponse({
                    'quiz_content': ai_response,
                    'credits_remaining': user.credits,
                    'topic': data['topic']
                })
                
            except Exception as e:
                user.add_credits(3)  # Refund
                return JsonResponse({'error': 'Quiz generation failed. Credits refunded.'}, status=500)
                
    except Exception as e:
        return JsonResponse({'error': 'Internal server error'}, status=500)

