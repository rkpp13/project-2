from django import forms
from .models import *

a,b,c,d,e = 'Fashion','Toys','Electronics','Home','Sports'
CATEGORIES = (
    ('None','No Category'),
    (a,a),(b,b),(c,c),(d,d),(e,e)
)
class ListingForm(forms.Form):
    title = forms.CharField(
        max_length=40,
        widget=forms.TextInput({'placeholder': 'Title','class': 'form-control'})
        )
    image = forms.URLField(
        required=False,
        widget=forms.URLInput({'placeholder': 'Image (optional)','class': 'form-control'})
        )
    category = forms.ChoiceField(
        choices=CATEGORIES,
        widget=forms.Select({'class': 'custom-select'})
        )
    description = forms.CharField(
        widget=forms.Textarea({'placeholder': 'Description','class': 'form-control'})
        )
    StartingBid = forms.DecimalField(
        min_value=1,
        widget=forms.NumberInput({'placeholder': 'Starting Bid','class': 'form-control'})
        )

class BidForm(forms.Form):
    bid = forms.DecimalField(
        widget=forms.NumberInput({'placeholder': 'Bid','class': 'form-control'})
    )

class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea({'placeholder': 'Comment goes here ...','class': 'form-control', 'rows':4})
    )
