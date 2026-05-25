"""
URL configuration for recipe project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView  # Required for the redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- HOMEPAGE REDIRECT ---
    # Redirects the root URL (/) to the album list
    path('', RedirectView.as_view(url='/albums/', permanent=False), name='home'),
    
    # --- NATIVE AUTHENTICATION ROUTING SYSTEM ---
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # We set next_page='login' so after logout, the user is sent back to the login screen 
    # and the message-clearing logic we added earlier is triggered.
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # --- CORE APPLICATION ROUTING ---
    # This includes the URLs defined in gallery/urls.py
    path('', include('gallery.urls')),
]

# Fallback media serving for local testing environments
if settings.DEBUG and not getattr(settings, 'USE_CLOUD_STORAGE', False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)