from django import forms
from .models import RecipePhoto

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = RecipePhoto
        fields = ['title', 'description', 'image']
        # Adding some basic Bootstrap classes for styling later
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., Spicy Tacos'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }