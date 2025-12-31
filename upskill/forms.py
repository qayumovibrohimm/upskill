from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 p-0', 'placeholder': 'Your Name'}
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 p-0', 'placeholder': 'Your Email'}
    ))
    subject = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 p-0', 'placeholder': 'Subject'}
    ))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control border-top-0 border-right-0 border-left-0 p-0', 'rows': 5, 'placeholder': 'Message'}
    ))
