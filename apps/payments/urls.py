from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create-checkout/', views.create_checkout, name='create_checkout'),
    path('webhook/', views.webhook, name='webhook'),
    path('success/', views.payment_success, name='success'),
    path('history/', views.payment_history, name='history'),
]

