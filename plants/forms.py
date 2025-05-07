from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'description', 'location', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }