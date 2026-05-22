from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Album(models.Model):
    """
    Groups individual photos together. Relates directly to a User 
    to enforce Role-Based Access Control (RBAC) rules.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Track the creator of the album to handle access permissions
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    
    # Architectural flag to separate administrative spaces from standard user spaces
    is_admin_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class RecipePhoto(models.Model):
    # Added null=True and blank=True to let Django bypass the mandatory entry check on older data fields
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = CloudinaryField('image')
    uploaded_at = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return f"{self.title} (Album: {self.album.title if self.album else 'None'})"