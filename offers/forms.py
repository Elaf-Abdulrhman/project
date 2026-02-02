from django import forms
from .models import Offer,Application

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'content', 'photo', 'email', 'url', 'phone_number','gender','date', 'location']


class ApplicationResponseForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'response_message']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'response_message': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Response to athlete...'}),
        }