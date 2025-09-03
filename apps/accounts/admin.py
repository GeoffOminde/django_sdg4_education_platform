from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AIInteraction, Payment, Subscription


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'credits', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email')
    ordering = ('-created_at',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Credits', {'fields': ('credits',)}),
    )


@admin.register(AIInteraction)
class AIInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'prompt_preview', 'model_used', 'credits_used', 'created_at')
    list_filter = ('model_used', 'credits_used', 'created_at')
    search_fields = ('user__username', 'prompt')
    readonly_fields = ('created_at',)
    
    def prompt_preview(self, obj):
        return obj.prompt[:50] + "..." if len(obj.prompt) > 50 else obj.prompt
    prompt_preview.short_description = 'Prompt'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'credits_purchased', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('user__username', 'intasend_payment_id')
    readonly_fields = ('created_at', 'completed_at')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_type', 'status', 'monthly_credits', 'price', 'expires_at')
    list_filter = ('plan_type', 'status', 'created_at')
    search_fields = ('user__username',)

