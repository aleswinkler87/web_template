from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['rocnik', 'name', 'description']
        labels = {
            'name': 'Vitez',  # Změna labelu pro pole "name"
        }