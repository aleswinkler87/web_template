from django import forms
from .models import Item, Comment

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['rocnik', 'name', 'description']
        labels = {
            'name': 'Vítěz',  # Změna labelu pro pole "name"
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            "text": "Napište komentář",
        }
