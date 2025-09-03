from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Extended user model with credits system"""
    email = models.EmailField(unique=True)
    credits = models.PositiveIntegerField(default=10)  # Free starter credits
    created_at = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def deduct_credits(self, amount=1):
        """Deduct credits if sufficient balance"""
        if self.credits >= amount:
            self.credits -= amount
            self.save()
            return True
        return False
    
    def add_credits(self, amount):
        """Add credits to user account"""
        self.credits += amount
        self.save()
    
    def __str__(self):
        return f"{self.username} ({self.credits} credits)"


class AIInteraction(models.Model):
    """Store AI tutor interactions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_interactions')
    prompt = models.TextField()
    response = models.TextField()
    model_used = models.CharField(max_length=100)
    credits_used = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.prompt[:50]}..."


class Payment(models.Model):
    """Track payments and credit purchases"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    intasend_payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    credits_purchased = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.credits_purchased} credits - {self.status}"


class Subscription(models.Model):
    """User subscriptions"""
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('institutional', 'Institutional'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    monthly_credits = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.username}: {self.plan_type} - {self.status}"

