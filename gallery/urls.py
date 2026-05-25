from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),

    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('album/new/', views.AlbumCreateView.as_view(), name='album_create'),
    path('album/<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album_update'),
    path('album/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album_delete'),
    
    path('album/<int:album_id>/upload/', views.PhotoCreateView.as_view(), name='photo_create'),
    path('photo/<int:pk>/edit/', views.PhotoUpdateView.as_view(), name='photo_update'),
    path('photo/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),
]