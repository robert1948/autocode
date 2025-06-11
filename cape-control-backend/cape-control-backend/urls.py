# --- File: cape_control_backend/urls.py ---
# Main URL configuration for the Django project.
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as auth_token_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')), # Djoser URLs for user registration, login etc.
    path('api/auth/', include('djoser.urls.authtoken')), # Djoser for token-based authentication
    path('api/', include('users.urls')), # Your custom user-related URLs (if any, like profile)
    path('api/', include('agents.urls')), # Your agent-related URLs
]