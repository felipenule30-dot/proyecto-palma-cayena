from django import forms
from .models import NewsletterSubscriber, ContactMessage


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Tu email'}),
            'name': forms.TextInput(attrs={'placeholder': 'Tu nombre (opcional)'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'placeholder': 'hola@tucorreo.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+57 300 000 0000'}),
            'subject': forms.TextInput(attrs={'placeholder': '¿En qué podemos ayudarte?'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escríbenos...'}),
        }
