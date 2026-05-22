"""
URL configuration for recipe project.
Production-Ready Authentication Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Import Django's native authentication system views for RBAC
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- NATIVE AUTHENTICATION ROUTING SYSTEM ---
    # Login route using Django's built-in view (searches for templates/registration/login.html)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Logout route handling account teardown hooks safely
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Forward all core application routes to your gallery application
    path('', include('gallery.urls')),
]

# Fallback media serving for local testing environments when Cloudinary is disabled
if settings.DEBUG and not getattr(settings, 'USE_CLOUD_STORAGE', False):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)