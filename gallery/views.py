from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm # Native user creation fields
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
import cloudinary.uploader
from .models import Album, RecipePhoto

# --- ACCOUNT REGISTRATION CONTROL ---
class SignUpView(CreateView):
    """
    Handles user account registration using Django's built-in creation form.
    """
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')  # Sends users straight to login after signup

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully! Please log in below.")
        return super().form_valid(form)


# --- ALBUM READ (LIST ALL ACCESSIBLE ALBUMS) ---
class AlbumListView(LoginRequiredMixin, ListView):
    """
    Renders all albums accessible to the logged-in user.
    Enforces RBAC by hiding administrator albums from regular accounts.
    """
    model = Album
    template_name = 'gallery/album_list.html'
    context_object_name = 'albums'
    paginate_by = 6  # Handles list paging automatically

    def get_queryset(self):
        # Admin / Staff can see everything; standard users only see public or standard items
        if self.request.user.is_staff:
            return Album.objects.all().order_by('-created_at')
        return Album.objects.filter(is_admin_only=False).order_by('-created_at')


# --- ALBUM DETAIL / GALLERY VIEW ---
class AlbumDetailView(LoginRequiredMixin, DetailView):
    """
    Renders an individual album page along with its associated photos.
    Includes filtering mechanisms to search for photos by title or description.
    """
    model = Album
    template_name = 'gallery/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        
        # Pull photos matching this specific parent album instance
        photo_queryset = self.object.photos.all().order_by('-uploaded_at')
        
        if query:
            photo_queryset = photo_queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            
        context['photos'] = photo_queryset
        context['query'] = query
        return context


# --- ALBUM CREATE CONTROL ---
class AlbumCreateView(LoginRequiredMixin, CreateView):
    """
    Allows authenticated users to group photos into newly declared collections.
    """
    model = Album
    fields = ['title', 'description', 'is_admin_only']
    template_name = 'gallery/album_form.html'
    success_url = reverse_lazy('album_list')

    def form_valid(self, form):
        # Silently tag the currently logged-in account as the creator
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Album '{form.instance.title}' created successfully!")
        return super().form_valid(form)


# --- PHOTO CREATE UPLOAD CONTROL ---
class PhotoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Saves an asset file into an explicit parent album target.
    RBAC: Prevents outside users from adding images to an album they don't own.
    """
    model = RecipePhoto
    fields = ['title', 'description', 'image']
    template_name = 'gallery/photo_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Fetch target parent album before executing standard validation checks
        self.album = get_object_or_404(Album, pk=self.kwargs['album_id'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        # RBAC Check: Ensure user owns this collection or belongs to the staff administration
        if self.album.is_admin_only and not self.request.user.is_staff:
            return False
        return self.album.created_by == self.request.user or self.request.user.is_staff

    def form_valid(self, form):
        form.instance.album = self.album
        messages.success(self.request, "Photo uploaded successfully to Cloudinary!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.album.pk})


# --- PHOTO UPDATE (EDIT) ---
class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Modifies existing title/description metadata text fields.
    """
    model = RecipePhoto
    fields = ['title', 'description']
    template_name = 'gallery/edit.html'
    context_object_name = 'photo'

    def test_func(self):
        photo = self.get_object()
        # Ensure modifying permissions match creation ownership
        return photo.album.created_by == self.request.user or self.request.user.is_staff

    def get_success_url(self):
        messages.success(self.request, "Photo details updated successfully.")
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})


# --- PHOTO DELETE CONTROL ---
class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Permanently eliminates records from PostgreSQL and triggers
    remote asset deletion commands to Cloudinary server arrays.
    """
    model = RecipePhoto
    template_name = 'gallery/delete.html'
    context_object_name = 'photo'

    def test_func(self):
        photo = self.get_object()
        return photo.album.created_by == self.request.user or self.request.user.is_staff

    def form_valid(self, form):
        photo = self.get_object()
        
        # Fire structural asset cleanup call targeting Cloudinary systems
        if photo.image:
            try:
                cloudinary.uploader.destroy(photo.image.public_id)
            except Exception as cloudinary_error:
                # Log issues gracefully without interrupting database synchronization loops
                print(f"Cloudinary deletion failed: {cloudinary_error}")
                
        messages.success(self.request, f"'{photo.title}' was permanently deleted.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.album.pk})