from re import I
from django import forms
from django.forms import ModelForm
from .models import Item, CURRENCY_CHOICES


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('currency',)
        widgets = {
            'currency': forms.Select(
                choices=CURRENCY_CHOICES, attrs={'class': 'form-control'}
            ),
        }
