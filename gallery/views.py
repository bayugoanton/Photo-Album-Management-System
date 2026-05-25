from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
import cloudinary.uploader
import logging
from .models import Album, RecipePhoto

logger = logging.getLogger(__name__)

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'gallery/album_list.html'
    context_object_name = 'albums'
    paginate_by = 6

class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        photos = self.object.photos.all().order_by('-uploaded_at')
        if query:
            photos = photos.filter(Q(title__icontains=query) | Q(description__icontains=query))
        context['photos'] = photos
        context['query'] = query
        return context

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['title', 'description', 'is_admin_only']
    template_name = 'gallery/album_form.html'
    success_url = reverse_lazy('album_list')

    # Add this method to link the user to the album
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Album created successfully.")
        return super().form_valid(form)

class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    fields = ['title', 'description', 'is_admin_only']
    template_name = 'gallery/album_form.html'
    success_url = reverse_lazy('album_list')
    def test_func(self):
        return self.get_object().created_by == self.request.user or self.request.user.is_staff

class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'gallery/delete.html'
    success_url = reverse_lazy('album_list')
    def test_func(self):
        return self.get_object().created_by == self.request.user or self.request.user.is_staff

class PhotoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = RecipePhoto
    fields = ['title', 'description', 'image']
    template_name = 'gallery/photo_form.html'
    def dispatch(self, request, *args, **kwargs):
        self.album = get_object_or_404(Album, pk=self.kwargs['album_id'])
        return super().dispatch(request, *args, **kwargs)
    def test_func(self):
        return self.album.created_by == self.request.user or self.request.user.is_staff
    def form_valid(self, form):
        form.instance.album = self.album
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.album.pk})

class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RecipePhoto
    fields = ['title', 'description']
    template_name = 'gallery/edit.html'
    def test_func(self):
        return self.get_object().album.created_by == self.request.user or self.request.user.is_staff
    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})

class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RecipePhoto
    template_name = 'gallery/delete.html'
    def test_func(self):
        return self.get_object().album.created_by == self.request.user or self.request.user.is_staff
    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})