import json
import hmac
import hashlib
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User, Payment


def verify_intasend_signature(payload, signature, secret):
    """Verify IntaSend webhook signature"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)


@login_required
@require_http_methods(["POST"])
def create_checkout(request):
    """Create IntaSend checkout session"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if 'credits' not in data:
        return JsonResponse({'error': 'Credits amount required'}, status=400)
    
    credits = int(data['credits'])
    
    # Credit pricing (in USD cents)
    pricing = {
        50: 500,   # $5.00 for 50 credits
        100: 900,  # $9.00 for 100 credits  
        500: 4000, # $40.00 for 500 credits
    }
    
    if credits not in pricing:
        return JsonResponse({'error': 'Invalid credit package'}, status=400)
    
    amount = pricing[credits]
    
    try:
        with transaction.atomic():
            # Create payment record
            payment = Payment.objects.create(
                user=request.user,
                intasend_payment_id=f"pending_{timezone.now().timestamp()}",
                amount=amount / 100,  # Convert to dollars
                credits_purchased=credits,
                status='pending'
            )
            
            # IntaSend checkout data
            checkout_data = {
                'public_key': settings.INTASEND_PUBLIC_KEY,
                'amount': amount,
                'currency': 'USD',
                'email': request.user.email,
                'first_name': request.user.username,
                'last_name': '',
                'host': settings.BASE_URL,
                'redirect_url': f"{settings.BASE_URL}/payments/success/",
                'api_ref': str(payment.id),
                'comment': f"Purchase {credits} credits"
            }
            
            return JsonResponse({
                'checkout_data': checkout_data,
                'payment_id': payment.id
            })
            
    except Exception as e:
        return JsonResponse({'error': 'Failed to create checkout'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def webhook(request):
    """Handle IntaSend payment webhooks"""
    signature = request.headers.get('X-Intasend-Signature')
    payload = request.body
    
    if not signature:
        return JsonResponse({'error': 'Missing signature'}, status=400)
    
    # Verify signature
    if not verify_intasend_signature(
        payload, 
        signature, 
        settings.INTASEND_WEBHOOK_SECRET
    ):
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    try:
        event_data = json.loads(payload.decode('utf-8'))
        
        if event_data.get('event') == 'payment.completed':
            payment_data = event_data.get('data', {})
            api_ref = payment_data.get('api_ref')
            
            if not api_ref:
                return JsonResponse({'error': 'Missing api_ref'}, status=400)
            
            with transaction.atomic():
                # Find payment record
                try:
                    payment = Payment.objects.select_for_update().get(id=int(api_ref))
                except Payment.DoesNotExist:
                    return JsonResponse({'error': 'Payment not found'}, status=404)
                
                if payment.status == 'completed':
                    return JsonResponse({'message': 'Already processed'}, status=200)
                
                # Update payment status
                payment.status = 'completed'
                payment.completed_at = timezone.now()
                payment.intasend_payment_id = payment_data.get('id', payment.intasend_payment_id)
                payment.save()
                
                # Add credits to user
                user = payment.user
                user.add_credits(payment.credits_purchased)
                
                return JsonResponse({'message': 'Payment processed successfully'}, status=200)
        
        return JsonResponse({'message': 'Event received'}, status=200)
        
    except Exception as e:
        return JsonResponse({'error': 'Webhook processing failed'}, status=500)


@login_required
def payment_success(request):
    """Payment success page"""
    return render(request, 'payments/success.html')


@login_required
def payment_history(request):
    """User payment history"""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/history.html', {'payments': payments})

