from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Album(models.Model):
    """
    Groups individual photos together. 
    The 'related_name' on the Album model allows us to easily access 
    user.albums.all() in our code.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='albums/', default='placeholder.jpg')
    
    # Track the creator of the album. 'db_index=True' makes filtering by user much faster.
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='albums',
        db_index=True 
    )
    
    is_admin_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at'] # Shows newest albums first by default


class RecipePhoto(models.Model):
    """
    Stores individual recipe photos linked to a specific Album.
    """
    album = models.ForeignKey(
        Album, 
        on_delete=models.CASCADE, 
        related_name='photos', 
        null=True, 
        blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        album_name = self.album.title if self.album else 'None'
        return f"{self.title} (Album: {album_name})"

    class Meta:
        ordering = ['-uploaded_at'] # Shows newest photos first