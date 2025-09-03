from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('pricing/', TemplateView.as_view(template_name='pricing.html'), name='pricing'),
    path('accounts/', include('apps.accounts.urls')),
    path('ai/', include('apps.ai_tutor.urls')),
    path('payments/', include('apps.payments.urls')),
    path('dashboard/', include('apps.accounts.urls')),  # Dashboard in accounts app
]

